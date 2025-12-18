"""API 路由模块"""
from app.api.predict import router as predict_router
from app.api.history import router as history_router

__all__ = ["predict_router", "history_router"]