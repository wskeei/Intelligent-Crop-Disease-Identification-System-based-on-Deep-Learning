
import torch
import torch.nn as nn
from torchvision.models.quantization import mobilenet_v3_large
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os
import json
import sys
from pathlib import Path


def get_quantizable_model(num_classes):
    # Instantiate Quantizable MobileNetV3
    # quantize=False means we get the Float model with Stubs, ready for QAT
    model = mobilenet_v3_large(weights=None, quantize=False)
    
    # Replace Classifier
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(in_features, num_classes)
    return model

def fix_model_advanced():
    print("Starting Advanced Model Fix (Fusion + Calibration)...")
    
    # 1. Setup
    backend = 'onednn' # Matches Windows CPU
    torch.backends.quantized.engine = backend
    print(f"Engine: {backend}")
    
    mapping_path = Path("backend/ml_models/class_mapping.json")
    with open(mapping_path, 'r') as f:
        classes = json.load(f)
    num_classes = len(classes)
    print(f"Num Classes: {num_classes}")

    # 2. Create Model
    model = get_quantizable_model(num_classes)
    
    # 3. Load Pre-trained Float Weights (Pruned or Base)
    # Prefer student_pruned.pth if available
    ckpt_path = Path("backend/training/student_pruned.pth")
    if not ckpt_path.exists():
        ckpt_path = Path("backend/training/student_base.pth")
    
    print(f"Loading weights from {ckpt_path}")
    checkpoint = torch.load(ckpt_path, map_location='cpu')
    if 'model_state_dict' in checkpoint:
        state_dict = checkpoint['model_state_dict']
    else:
        state_dict = checkpoint
        
    # Load weights (strict=False because QuantizableModel has extra 'quant' module keys that are missing in standard model)
    model.load_state_dict(state_dict, strict=False)
    
    # 4. Fuse Modules
    print("Fusing Conv+BN layers...")
    model.fuse_model(is_qat=True)
    
    # 5. Prepare QAT
    model.train()
    model.qconfig = torch.ao.quantization.get_default_qat_qconfig(backend)
    torch.ao.quantization.prepare_qat(model, inplace=True)
    print("Model prepared for QAT.")
    
    # 6. Calibration
    print("Calibrating on local data (1 epoch)...")
    data_dir = Path("backend/training/data")
    if not data_dir.exists():
        print("Error: content of data dir missing or not found")
        return

    # Use standard transform
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    dataset = datasets.ImageFolder(str(data_dir), transform=transform)
    # Use smaller subset for speed? No, run full or partial.
    # Run 50 batches is enough for calibration
    loader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    print(f"Dataset size: {len(dataset)}")
    
    device = torch.device('cpu') # QAT on CPU for safety with onednn
    model.to(device)
    
    # We don't need to optimize, just Forward pass to update observers
    with torch.no_grad():
        count = 0
        max_batches = 50
        for images, _ in loader:
            images = images.to(device)
            model(images)
            count += 1
            if count >= max_batches:
                break
                
    print("Calibration complete.")
    
    # 7. Convert
    print("Converting to Quantized Model...")
    model.eval()
    model.to('cpu')
    quantized_model = torch.ao.quantization.convert(model, inplace=False)
    
    # 8. Script & Save
    save_path = Path("backend/ml_models/quantized_model_scripted.pt")
    scripted_model = torch.jit.script(quantized_model)
    torch.jit.save(scripted_model, save_path)
    print(f"Saved Fixed Fused Model to {save_path}")

if __name__ == "__main__":
    fix_model_advanced()
