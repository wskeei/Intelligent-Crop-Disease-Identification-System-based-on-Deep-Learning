"""
预测相关的 Pydantic 模型
用于请求/响应数据验证
"""
from datetime import datetime
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """预测请求（用于文档说明，实际使用 UploadFile）"""
    pass


class PredictionResponse(BaseModel):
    """预测响应"""
    predicted_class: str  # 预测的病害类别
    confidence: float     # 置信度 (0-1)
    image_url: str        # 图片访问路径
    
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