import torch
import torch.nn as nn
from torchvision import models
import os

def get_student_model(num_classes):
    """
    Returns MobileNetV3 Large (which has SE blocks by default) as the student model.
    """
    # MobileNetV3 large already contains SE (Squeeze-and-Excitation) blocks
    model = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.IMAGENET1K_V1)
    
    # Modify the classifier to match the number of classes
    # MobileNetV3 classifier structure: Sequential(Linear, Hardswish, Dropout, Linear)
    # We need to replace the last Linear layer
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(in_features, num_classes)
    
    return model

def get_teacher_model(num_classes, weights_path=None):
    """
    Returns ResNet50 as the teacher model.
    If weights_path is provided, loads the state dict.
    """
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
    
    # Replace the fully connected layer
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(model.fc.in_features, num_classes)
    )
    
    if weights_path and os.path.exists(weights_path):
        print(f"Loading teacher weights from {weights_path}")
        checkpoint = torch.load(weights_path, map_location='cpu')
        
        # Handle cases where checkpoint might be the full state or just the model state
        if 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        else:
            state_dict = checkpoint
            
        model.load_state_dict(state_dict)
    else:
        print("Warning: No pre-trained weights found for Teacher, utilizing ImageNet weights only (with random head)")

    # Freeze teacher parameters so they don't update during distillation
    for param in model.parameters():
        param.requires_grad = False
        
    model.eval()
    return model
