import argparse
import os
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import time
import copy

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

def train_one_epoch(model, teacher, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for images, labels in loader:
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
        
    return running_loss / len(loader), 100. * correct / total

def validate(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    return 100. * correct / total

def main():
    args = get_args()
    if torch.cuda.is_available():
        device = torch.device('cuda')
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
    else:
        device = torch.device('cpu')
    print(f"Using device: {device}")
    
    # Set quantization engine dynamically
    import platform
    machine = platform.machine().lower()
    if 'arm' in machine or 'aarch64' in machine:
        torch.backends.quantized.engine = 'qnnpack'
    else:
        # x86_64 typically uses fbgemm
        torch.backends.quantized.engine = 'fbgemm'
    print(f"Using quantization engine: {torch.backends.quantized.engine}")
    
    # 1. Data Setup
    print("Setting up data...")
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    full_dataset = datasets.ImageFolder(args.data_dir, transform=transform)
    num_classes = len(full_dataset.classes)
    print(f"Detected {num_classes} classes.")
    
    # Split
    train_size = int(0.8 * len(full_dataset))
    val_size = len(full_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(full_dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False, num_workers=2)
    
    # 2. Model Setup
    print("Setting up models...")
    student = get_student_model(num_classes).to(device)
    teacher = get_teacher_model(num_classes, args.teacher_weights).to(device)
    
    criterion = KnowledgeDistillationLoss(alpha=0.5, temperature=3.0)
    optimizer = optim.Adam(student.parameters(), lr=args.lr)
    
    epochs = 1 if args.debug else args.epochs
    
    # 3. Phase 1: Distillation Training
    print("\n--- Phase 1: Knowledge Distillation Training ---")
    best_acc = 0.0
    for epoch in range(epochs):
        loss, acc = train_one_epoch(student, teacher, train_loader, criterion, optimizer, device)
        val_acc = validate(student, val_loader, device)
        print(f"Epoch {epoch+1}/{epochs} - Loss: {loss:.4f}, Train Acc: {acc:.2f}%, Val Acc: {val_acc:.2f}%")
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(student.state_dict(), "student_base.pth")
    
    # Ensure file exists for subsequent steps (important for debug/first run)
    if not os.path.exists("student_base.pth"):
         torch.save(student.state_dict(), "student_base.pth")
    
    # Load best base model
    student.load_state_dict(torch.load("student_base.pth", weights_only=True))
    print(f"Best Base Acc: {best_acc:.2f}%")
    
    # 4. Phase 2: Pruning
    print("\n--- Phase 2: Structured Pruning ---")
    apply_structured_pruning(student, amount=args.prune_amount)
    
    # Fine-tune after pruning (Distillation again)
    print("Fine-tuning pruned model...")
    optimizer = optim.Adam(student.parameters(), lr=args.lr * 0.1) # Lower LR
    for epoch in range(epochs // 2): # Less epochs for fine-tuning
        loss, acc = train_one_epoch(student, teacher, train_loader, criterion, optimizer, device)
        val_acc = validate(student, val_loader, device)
        print(f"Prune FT Epoch {epoch+1} - Val Acc: {val_acc:.2f}%")
        
    # Make pruning permanent
    remove_pruning_reparameterization(student)
    torch.save(student.state_dict(), "student_pruned.pth")
    
    # 5. Phase 3: Quantization Aware Training (QAT)
    print("\n--- Phase 3: Quantization Aware Training (QAT) ---")
    # QAT typically runs on CPU or via specific backends, but PyTorch QAT can simulate on GPU.
    # However, for correct conversion, we often stick to CPU or handle carefully.
    # We will try to keep on the current device (likely CPU for this user environment or MPS if Mac).
    # Note: QAT on MPS might have issues, check compatibility. Fallback to CPU for QAT safety often recommended.
    
    student.to('cpu') 
    teacher.to('cpu') # Teacher must match device if we use it for loss, though strict QAT usually just uses CE.
    # We will use simple CrossEntropy for QAT to avoid complexity of Teacher on specific QAT device constraints.
    criterion_qat = torch.nn.CrossEntropyLoss()
    
    # Prepare
    student.train() 
    student = prepare_model_for_qat(student)
    optimizer = optim.Adam(student.parameters(), lr=args.lr * 0.01)
    
    print("Fine-tuning for QAT (using standard CE loss)...")
    student.train()
    for epoch in range(epochs // 2):
        running_loss = 0.0
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = student(images)
            loss = criterion_qat(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"QAT Epoch {epoch+1} - Loss: {running_loss/len(train_loader):.4f}")
    
    # Convert
    quantized_model = convert_qat_model(student)
    
    # Verify Quantized Model
    print("Verifying Quantized Model Accuracy...")
    quantized_model.eval()
    q_acc = validate(quantized_model, val_loader, device='cpu')
    print(f"Quantized Model Accuracy: {q_acc:.2f}%")
    
    # Save
    torch.save(quantized_model.state_dict(), "quantized_mobilenet_se.pth")
    # Also save as TorchScript for easier deployment if needed, 
    # but state_dict is fine for our app loader structure if we reconstruct.
    try:
        scripted_model = torch.jit.script(quantized_model)
        torch.jit.save(scripted_model, "quantized_model_scripted.pt")
        print("Saved scripted quantized model.")
    except Exception as e:
        print(f"Could not script model: {e}")
        
    print("\nPipeline Complete!")

if __name__ == '__main__':
    main()
