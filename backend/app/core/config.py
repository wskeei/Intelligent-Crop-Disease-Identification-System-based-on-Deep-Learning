"""
应用配置模块
使用 pydantic-settings 管理环境变量和配置
"""
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基本信息
    APP_NAME: str = "CropVision-AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # 路径配置
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    MODEL_DIR: Path = BASE_DIR / "ml_models"
    
    # 模型配置
    MODEL_PATH: str = "best_model.pth"
    CLASS_MAPPING_PATH: str = "class_mapping.json"
    
    # Auth 配置
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./cropvision.db"
    
    # CORS 配置
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"]
    
    class Config:
        env_file = ".env"


# 全局配置实例
settings = Settings()

# 确保目录存在
settings.UPLOAD_DIR.mkdir(exist_ok=True)
settings.MODEL_DIR.mkdir(exist_ok=True)