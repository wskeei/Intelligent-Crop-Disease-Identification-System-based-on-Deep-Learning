"""
预测 API 路由
处理图片上传和病害识别
"""
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.prediction import PredictionRecord
from app.schemas.prediction import PredictionResponse
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api", tags=["预测"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(
    file: UploadFile = File(..., description="上传的农作物图片"),
    db: AsyncSession = Depends(get_db)
):
    """
    上传图片进行病害识别
    
    - **file**: 农作物叶片图片 (支持 jpg, png, webp)
    
    返回预测的病害类别和置信度
    """
    # 验证文件类型
    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="仅支持 jpg/png/webp 格式图片")
    
    # 保存上传的图片
    file_ext = Path(file.filename).suffix or ".jpg"
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = settings.UPLOAD_DIR / filename
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    # 执行预测
    predicted_class, confidence, top_predictions = ai_service.predict(file_path)
    
    # 保存记录到数据库
    record = PredictionRecord(
        image_path=str(filename),
        predicted_class=predicted_class,
        confidence=confidence
    )
    db.add(record)
    await db.commit()
    
    return PredictionResponse(
        predicted_class=predicted_class,
        confidence=round(confidence, 4),
        image_url=f"/uploads/{filename}",
        top_predictions=top_predictions
    )