"""Pydantic 数据验证模型"""
from app.schemas.prediction import PredictionRequest, PredictionResponse, PredictionHistoryResponse

__all__ = ["PredictionRequest", "PredictionResponse", "PredictionHistoryResponse"]