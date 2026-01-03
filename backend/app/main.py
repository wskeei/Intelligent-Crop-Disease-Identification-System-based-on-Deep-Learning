"""
CropVision-AI 后端主入口
FastAPI 应用启动配置
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import init_db
from app.core.database import init_db
from app.api import predict_router, history_router, auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    print(f"🌾 {settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
    yield
    # 关闭时清理资源
    print("👋 应用关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于深度学习的农作物病害智能识别系统 API",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录（用于访问上传的图片）
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 注册路由
app.include_router(predict_router)
app.include_router(history_router)
app.include_router(auth_router)


@app.get("/", tags=["健康检查"])
async def root():
    """API 根路径，返回服务状态"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}