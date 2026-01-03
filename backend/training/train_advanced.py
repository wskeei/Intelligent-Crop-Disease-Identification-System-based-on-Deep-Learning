import argparse
import os
import sys
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import time
import copy
import matplotlib.pyplot as plt
import requests
import zipfile
import shutil
from tqdm import tqdm

# Import our modules
from models import get_student_model, get_teacher_model
from distillation import KnowledgeDistillationLoss
from pruning import apply_structured_pruning, remove_pruning_reparameterization
from quantization import prepare_model_for_qat, convert_qat_model

def get_args():
    parser = argparse.ArgumentParser(description='Advanced Crop Disease Training Pipeline')
    parser.add_argument('--data_dir', type=str, required=True, help='Path to dataset')
    parser.add_argument('--teacher_weights', type=str, default='../ml_models/best_model.pth', help='Path to teacher weights')
    parser.add_argument('--epochs', type=int, default=20, help='Number of epochs for each phase')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--prune_amount', type=float, default=0.2, help='Amount of structured pruning')
    parser.add_argument('--debug', action='store_true', help='Debug mode (1 epoch)')
    return parser.parse_args()

def download_and_extract_dataset(data_dir):
    """Downloads PlantVillage dataset if not present."""
    plantvillage_dir = os.path.join(data_dir, 'PlantVillage')
    
    # Check if data exists (naive check: directory exists and has subfolders)
    if os.path.exists(plantvillage_dir):
        if len(os.listdir(plantvillage_dir)) > 2:
            print(f"[INFO] Dataset found at {plantvillage_dir}")
            return plantvillage_dir

    print(f"[INFO] Dataset not found in {data_dir}. Downloading...")
    os.makedirs(data_dir, exist_ok=True)
    
    url = "https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip"
    zip_path = os.path.join(data_dir, "plantvillage.zip")
    
    # Download
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        block_size = 8192
        with open(zip_path, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=block_size), total=total_size//block_size, unit='KB', desc="Downloading"):
                f.write(chunk)
                
    # Extract
    print("[INFO] Extracting dataset...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_dir)
        
    # Organize: Move raw/color/* to data_dir/PlantVillage
    extracted_root = os.path.join(data_dir, "PlantVillage-Dataset-master")
    source_imgs = os.path.join(extracted_root, "raw", "color")
    
    if os.path.exists(source_imgs):
        # We rename 'color' to 'PlantVillage' effectively
        # Or move contents. Let's move contents to data_dir/PlantVillage
        if os.path.exists(plantvillage_dir):
            shutil.rmtree(plantvillage_dir)
        shutil.move(source_imgs, plantvillage_dir)
        
    # Cleanup
    try:
        os.remove(zip_path)
        shutil.rmtree(extracted_root)
    except Exception as e:
        print(f"[WARN] Cleanup failed: {e}")
        
    print(f"[INFO] Dataset ready at {plantvillage_dir}")
    return plantvillage_dir

def save_plots(history, filename="training_plot.png"):
    """Saves training history plots."""
    epochs = [x['epoch'] for x in history]
    train_loss = [x['train_loss'] for x in history]
    val_acc = [x['val_acc'] for x in history]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    color = 'tab:red'
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss', color=color)
    ax1.plot(epochs, train_loss, color=color, label='Train Loss', marker='o')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)
    
    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Accuracy (%)', color=color)
    ax2.plot(epochs, val_acc, color=color, label='Val Acc', marker='s')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('Training Progress')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"[INFO] Plot saved to {filename}")

def train_one_epoch(model, teacher, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(loader, desc="Training", leave=False)
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        optimizer.zero_grad()
        
        # Student forward
        student_logits = model(images)
        
        # Teacher forward (no grad)
        with torch.no_grad():
            teacher_logits = teacher(images)
            
        # Calculate Loss
        loss = criterion(student_logits, teacher_logits, labels)
        
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = student_logits.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({'loss': loss.item()})
        
    return running_loss / len(loader), 100. * correct / total

def validate(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in tqdm(loader, desc="Validating", leave=False):
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    return 100. * correct / total

def main():
    args = get_args()
    
    # Logs directory
    os.makedirs("runs", exist_ok=True)
    
    if torch.cuda.is_available():
        device = torch.device('cuda')
        print(f"[INFO] GPU Detected: {torch.cuda.get_device_name(0)}")
        print(f"[INFO] VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
        print("[INFO] MPS (Apple Silicon) Detected.")
    else:
        device = torch.device('cpu')
        print("[WARN] GPU not found! Training will be slow.")
    print(f"Using device: {device}")
    
    # Set quantization engine dynamically
    # [FIX] Force qnnpack on Windows/x86 simply because fbgemm can be unstable for some PyTorch versions on specific CPUs
    # or if there's a mismatch. qnnpack is safer.
    torch.backends.quantized.engine = 'fbgemm'
    print(f"[INFO] Quantization engine: {torch.backends.quantized.engine}")
    
    # 1. Data Setup
    print("\n[STEP 1/5] Setting up Data...")
    # Handle download automatically
    dataset_path = download_and_extract_dataset(args.data_dir)
    
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    full_dataset = datasets.ImageFolder(dataset_path, transform=transform)
    num_classes = len(full_dataset.classes)
    print(f"[INFO] Found {num_classes} classes.")
    
    # Split
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    
    num_workers = 2 # Optimized for Windows, changed from 4
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)
    
    # 2. Model Setup
    print("\n[STEP 2/5] Initializing Models...")
    student = get_student_model(num_classes).to(device)
    try:
        teacher = get_teacher_model(num_classes, args.teacher_weights).to(device)
        print("[INFO] Teacher weights loaded.")
    except Exception as e:
        print(f"[WARN] Could not load teacher weights: {e}")
        print("[WARN] Using un-trained teacher (not recommended for distillation performance).")
        teacher = get_teacher_model(num_classes, None).to(device)
    
    criterion = KnowledgeDistillationLoss(alpha=0.5, temperature=3.0)
    optimizer = optim.Adam(student.parameters(), lr=args.lr)
    
    epochs = 1 if args.debug else args.epochs
    history = []
    
    # RESUME LOGIC CHECKS
    skip_phase1 = False
    skip_phase2 = False
    
    if os.path.exists("student_pruned.pth"):
        print("\n[RESUME] Found 'student_pruned.pth'. Skipping Phase 1 (Distillation) and Phase 2 (Pruning).")
        skip_phase1 = True
        skip_phase2 = True
        
    elif os.path.exists("student_base.pth"):
        print("\n[RESUME] Found 'student_base.pth'. Skipping Phase 1 (Distillation).")
        skip_phase1 = True
        
    # 3. Phase 1: Distillation Training
    if not skip_phase1:
        print(f"\n[STEP 3/5] Starting Distillation Training ({epochs} epochs)...")
        best_acc = 0.0
        for epoch in range(epochs):
            start_time = time.time()
            loss, acc = train_one_epoch(student, teacher, train_loader, criterion, optimizer, device)
            val_acc = validate(student, val_loader, device)
            
            epoch_time = time.time() - start_time
            print(f"Epoch {epoch+1}/{epochs} | Time: {epoch_time:.1f}s | Loss: {loss:.4f} | TrainAcc: {acc:.2f}% | ValAcc: {val_acc:.2f}%")
            
            history.append({'epoch': epoch+1, 'train_loss': loss, 'val_acc': val_acc})
            save_plots(history, "runs/distillation_plot.png")
            
            if val_acc > best_acc:
                best_acc = val_acc
                torch.save(student.state_dict(), "student_base.pth")
                print(f" >> Saved New Best Model (Acc: {val_acc:.2f}%)")
                
        # Ensure student_base.pth exists even if best_acc wasn't updated (e.g., debug mode 1 epoch)
        if not os.path.exists("student_base.pth"):
             torch.save(student.state_dict(), "student_base.pth")

        # Load best base model
        student.load_state_dict(torch.load("student_base.pth", weights_only=True))
        print(f"[INFO] Loaded best student_base.pth (Acc: {best_acc:.2f}%)")
    else:
        if not skip_phase2: # If we only skipped phase 1, load student_base.pth
             print("[INFO] Loading student_base.pth...")
             student.load_state_dict(torch.load("student_base.pth", weights_only=True))
        # If skip_phase2 is also true, we will load student_pruned.pth later.
    
    # 4. Phase 2: Pruning
    if not skip_phase2:
        print("\n[STEP 4/5] Structured Pruning & Fine-tuning...")
        apply_structured_pruning(student, amount=args.prune_amount)
        
        optimizer = optim.Adam(student.parameters(), lr=args.lr * 0.1) # Lower LR
        ft_epochs = max(1, epochs // 2)
        
        for epoch in range(ft_epochs):
            loss, acc = train_one_epoch(student, teacher, train_loader, criterion, optimizer, device)
            val_acc = validate(student, val_loader, device)
            print(f"Prune FT Epoch {epoch+1}/{ft_epochs} | Val Acc: {val_acc:.2f}%")
            
        remove_pruning_reparameterization(student)
        torch.save(student.state_dict(), "student_pruned.pth")
        print("[INFO] Saved student_pruned.pth")
    else:
        print("[INFO] Loading student_pruned.pth for QAT...")
        # Since the saved model has pruning made permanent, it's just a normal model with sparse weights
        student.load_state_dict(torch.load("student_pruned.pth", weights_only=True))
    
    # 5. Phase 3: Quantization Aware Training (QAT)
    print("\n[STEP 5/5] Quantization Aware Training (QAT)...")
    
    # Move to CPU for safe QAT
    print("[INFO] Moving model to CPU for QAT stability...")
    student.to('cpu') 
    teacher.to('cpu') # Also move teacher to CPU
    criterion_qat = torch.nn.CrossEntropyLoss()
    
    student.train() 
    student = prepare_model_for_qat(student)
    optimizer = optim.Adam(student.parameters(), lr=args.lr * 0.01)
    
    print("Fine-tuning for QAT (using standard CE loss)...")
    ft_epochs_qat = max(1, epochs // 2)
    for epoch in range(ft_epochs_qat):
        running_loss = 0.0
        pbar = tqdm(train_loader, desc=f"QAT Epoch {epoch+1}", leave=False)
        for images, labels in pbar:
            # Images need to be on CPU now
            optimizer.zero_grad()
            outputs = student(images)
            loss = criterion_qat(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            pbar.set_postfix({'loss': loss.item()})
        print(f"QAT Epoch {epoch+1} - Loss: {running_loss/len(train_loader):.4f}")
    
    # Convert
    quantized_model = convert_qat_model(student)
    
    # Verify Quantized Model
    print("Verifying Quantized Model Accuracy...")
    try:
        quantized_model.eval()
        q_acc = validate(quantized_model, val_loader, device='cpu')
        print(f"Quantized Model Accuracy: {q_acc:.2f}%")
    except Exception as e:
        print(f"[WARNING] Verification Failed: {e}")
        print("Continuing to save model anyway...")
    
    # Save
    save_path = "quantized_mobilenet_se.pth"
    torch.save(quantized_model.state_dict(), save_path)
    print(f"\n[SUCCESS] Pipeline Complete! Final Model: {save_path}")

    try:
        scripted_model = torch.jit.script(quantized_model)
        torch.jit.save(scripted_model, "quantized_model_scripted.pt")
        print("[INFO] Saved scripted quantized model to quantized_model_scripted.pt")
    except Exception as e:
        print(f"[WARNING] Could not script model: {e}")
        
    print("\nPipeline Complete!")

if __name__ == '__main__':
    main()
