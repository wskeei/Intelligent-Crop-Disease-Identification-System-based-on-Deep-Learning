"""
AI 推理服务
单例模式加载模型，提供病害预测功能
"""
import json
from pathlib import Path
from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms, models

from app.core.config import settings


class AIService:
    """AI 推理服务（单例模式）"""
    
    _instance = None
    _model = None
    _class_mapping = None
    _transform = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            self._load_model()
            self._setup_transform()
    
    def _load_model(self):
        """加载训练好的模型"""
        model_path = settings.MODEL_DIR / settings.MODEL_PATH
        mapping_path = settings.MODEL_DIR / settings.CLASS_MAPPING_PATH
        
        # 检查模型文件是否存在
        if not model_path.exists():
            print(f"警告: 模型文件不存在 {model_path}，使用模拟模式")
            self._class_mapping = {str(i): f"Disease_{i}" for i in range(38)}
            return
        
        # 加载类别映射
        if mapping_path.exists():
            with open(mapping_path, "r") as f:
                self._class_mapping = json.load(f)
        else:
            self._class_mapping = {str(i): f"Disease_{i}" for i in range(38)}
        
        # 加载模型
        checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
        num_classes = checkpoint.get("num_classes", len(self._class_mapping))
        
        # 构建模型结构
        self._model = models.resnet50(weights=None)
        self._model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(self._model.fc.in_features, num_classes)
        )
        self._model.load_state_dict(checkpoint["model_state_dict"])
        self._model.eval()
        
        # 更新类别映射
        if "classes" in checkpoint:
            self._class_mapping = {str(i): name for i, name in enumerate(checkpoint["classes"])}
    
    def _setup_transform(self):
        """设置图像预处理"""
        self._transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    def predict(self, image_path: Path) -> tuple[str, float]:
        """
        对图片进行病害预测
        
        Args:
            image_path: 图片路径
            
        Returns:
            (预测类别, 置信度)
        """
        # 加载并预处理图片
        image = Image.open(image_path).convert("RGB")
        input_tensor = self._transform(image).unsqueeze(0)
        
        # 模拟模式（模型未加载时）
        if self._model is None:
            import random
            idx = random.randint(0, len(self._class_mapping) - 1)
            return self._class_mapping[str(idx)], random.uniform(0.7, 0.99)
        
        # 推理
        with torch.no_grad():
            outputs = self._model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
        
        predicted_class = self._class_mapping.get(str(predicted_idx.item()), "Unknown")
        return predicted_class, confidence.item()


# 全局服务实例
ai_service = AIService()