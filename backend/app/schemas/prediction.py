"""
预测相关的 Pydantic 模型
用于请求/响应数据验证
"""
from datetime import datetime
from pydantic import BaseModel


class TopPrediction(BaseModel):
    """单个预测结果"""
    class_name: str  # 使用 class_name 避免与 Python 关键字冲突
    confidence: float

    class Config:
        # 允许从 dict 的 "class" 字段映射
        populate_by_name = True


class PredictionResponse(BaseModel):
    """预测响应"""
    predicted_class: str  # 预测的病害类别
    confidence: float     # 置信度 (0-1)
    image_url: str        # 图片访问路径
    top_predictions: list[dict]  # Top-3 预测结果
    
    class Config:
        from_attributes = True


class PredictionHistoryResponse(BaseModel):
    """历史记录响应"""
    id: int
    image_path: str
    predicted_class: str
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True