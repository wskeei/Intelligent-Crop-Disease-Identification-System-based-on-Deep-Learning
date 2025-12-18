"""
历史记录 API 路由
查询识别历史
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.prediction import PredictionRecord
from app.schemas.prediction import PredictionHistoryResponse

router = APIRouter(prefix="/api", tags=["历史记录"])


@router.get("/history", response_model=list[PredictionHistoryResponse])
async def get_history(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取识别历史记录
    
    - **skip**: 分页偏移量
    - **limit**: 每页数量 (最大100)
    """
    query = select(PredictionRecord).order_by(
        PredictionRecord.created_at.desc()
    ).offset(skip).limit(limit)
    
    result = await db.execute(query)
    records = result.scalars().all()
    return records


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """
    获取统计数据
    
    返回各类病害的识别次数统计
    """
    # 总记录数
    total_query = select(func.count(PredictionRecord.id))
    total_result = await db.execute(total_query)
    total = total_result.scalar()
    
    # 按类别统计
    stats_query = select(
        PredictionRecord.predicted_class,
        func.count(PredictionRecord.id).label("count")
    ).group_by(PredictionRecord.predicted_class)
    
    stats_result = await db.execute(stats_query)
    class_stats = [{"class": row[0], "count": row[1]} for row in stats_result.all()]
    
    return {"total": total, "by_class": class_stats}