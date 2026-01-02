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
import torch.quantization


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
    
        if "classes" in checkpoint:
            self._class_mapping = {str(i): name for i, name in enumerate(checkpoint["classes"])}

    def _load_mobilenet_quantized(self):
        """Try to load the new quantized MobileNetV3 model"""
        # Define paths for new model (this is a placeholder logic, usually we'd have a config switch)
        # For now, we will add a check in _load_model to prefer this if it exists
        pass

    def _load_model(self):
        """加载训练好的模型"""
        # Prioritize Quantized Utils if available
        quantized_path = settings.MODEL_DIR / "quantized_model_scripted.pt" 
        # Or state dict path
        quantized_state_path = settings.MODEL_DIR / "quantized_mobilenet_se.pth"
        
        mapping_path = settings.MODEL_DIR / settings.CLASS_MAPPING_PATH
        model_path = settings.MODEL_DIR / settings.MODEL_PATH # Fallback old model

        # Load Mapping
        if mapping_path.exists():
            with open(mapping_path, "r") as f:
                self._class_mapping = json.load(f)
        else:
            self._class_mapping = {str(i): f"Disease_{i}" for i in range(38)}
            
        # Try loading Quantized Script Model first (Fastest)
        if quantized_path.exists():
            print(f"Loading Quantized Model (Scripted) from {quantized_path}")
            try:
                self._model = torch.jit.load(quantized_path)
                self._model.eval()
                print("Quantized Model Loaded Successfully")
                return
            except Exception as e:
                print(f"Failed to load scripted model: {e}")

        # Try loading Quantized State Dict
        if quantized_state_path.exists():
             print(f"Loading Quantized Model (State Dict) from {quantized_state_path}")
             try:
                 # Reconstruct Model Structure
                 from torchvision.models import mobilenet_v3_large
                 model = mobilenet_v3_large(weights=None)
                 num_classes = len(self._class_mapping)
                 model.classifier[3] = nn.Linear(model.classifier[3].in_features, num_classes)
                 
                 # Prepare for QAT/Quantization structure matches
                 model.qconfig = torch.ao.quantization.get_default_qat_qconfig('fbgemm')
                 torch.ao.quantization.prepare_qat(model, inplace=True)
                 torch.ao.quantization.convert(model, inplace=True)
                 
                 model.load_state_dict(torch.load(quantized_state_path, map_location='cpu'))
                 self._model = model
                 self._model.eval()
                 return
             except Exception as e:
                 print(f"Failed to load quantized state dict: {e}")

        # Fallback to Original ResNet50
        print(f"Loading Standard Model from {model_path}")
        if not model_path.exists():
            print(f"警告: 模型文件不存在 {model_path}，使用模拟模式")
            return
        
        checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
        num_classes = checkpoint.get("num_classes", len(self._class_mapping))
        
        self._model = models.resnet50(weights=None)
        self._model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(self._model.fc.in_features, num_classes)
        )
        self._model.load_state_dict(checkpoint["model_state_dict"])
        self._model.eval()
        
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
    
    def predict(self, image_path: Path) -> tuple[str, float, list[dict]]:
        """
        对图片进行病害预测
        
        Args:
            image_path: 图片路径
            
        Returns:
            (预测类别, 置信度, Top-3预测列表)
        """
        # 加载并预处理图片
        image = Image.open(image_path).convert("RGB")
        input_tensor = self._transform(image).unsqueeze(0)
        
        # 模拟模式（模型未加载时）
        if self._model is None:
            import random
            idx = random.randint(0, len(self._class_mapping) - 1)
            conf = random.uniform(0.7, 0.99)
            top_predictions = [{"class": self._class_mapping[str(idx)], "confidence": round(conf, 4)}]
            return self._class_mapping[str(idx)], conf, top_predictions
        
        # 推理
        with torch.no_grad():
            outputs = self._model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            top3_conf, top3_idx = torch.topk(probabilities, k=min(3, probabilities.size(1)), dim=1)
        
        # 构建 Top-3 结果
        top_predictions = []
        for i in range(top3_idx.size(1)):
            cls_name = self._class_mapping.get(str(top3_idx[0, i].item()), "Unknown")
            top_predictions.append({"class": cls_name, "confidence": round(top3_conf[0, i].item(), 4)})
        
        predicted_class = top_predictions[0]["class"]
        confidence = top_predictions[0]["confidence"]
        return predicted_class, confidence, top_predictions


# 全局服务实例
ai_service = AIService()