"""
历史记录 API 路由
查询识别历史
"""
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, func, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.prediction import PredictionRecord
from app.schemas.prediction import PredictionHistoryResponse
import os

router = APIRouter(prefix="/api", tags=["历史记录"])


class BatchDeleteRequest(BaseModel):
    ids: list[int]


@router.get("/history", response_model=list[PredictionHistoryResponse])
async def get_history(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回记录数"),
    db: AsyncSession = Depends(get_db)
):
    """获取识别历史记录"""
    query = select(PredictionRecord).order_by(
        PredictionRecord.created_at.desc()
    ).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/history/{id}", response_model=PredictionHistoryResponse)
async def get_history_detail(id: int, db: AsyncSession = Depends(get_db)):
    """获取单条识别记录详情"""
    result = await db.execute(select(PredictionRecord).where(PredictionRecord.id == id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record


@router.delete("/history/batch")
async def batch_delete_history(req: BatchDeleteRequest, db: AsyncSession = Depends(get_db)):
    """批量删除识别记录"""
    """批量删除识别记录"""
    # 先查询要删除的记录以获取文件名
    query = select(PredictionRecord).where(PredictionRecord.id.in_(req.ids))
    result = await db.execute(query)
    records = result.scalars().all()
    
    # 删除文件
    deleted_files_count = 0
    for record in records:
        if record.image_path:
            file_path = settings.UPLOAD_DIR / record.image_path
            try:
                if file_path.exists():
                    os.remove(file_path)
                    deleted_files_count += 1
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

    # 删除数据库记录
    result = await db.execute(
        delete(PredictionRecord).where(PredictionRecord.id.in_(req.ids))
    )
    await db.commit()
    return {"success": True, "deleted_count": result.rowcount, "deleted_files": deleted_files_count}


@router.delete("/history/{id}")
async def delete_history(id: int, db: AsyncSession = Depends(get_db)):
    """删除单条识别记录"""
    result = await db.execute(select(PredictionRecord).where(PredictionRecord.id == id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    # 删除关联的图片文件
    if record.image_path:
        file_path = settings.UPLOAD_DIR / record.image_path
        try:
            if file_path.exists():
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    await db.delete(record)
    await db.commit()
    return {"success": True, "message": "删除成功"}


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """获取增强统计数据"""
    # 总记录数
    total = (await db.execute(select(func.count(PredictionRecord.id)))).scalar() or 0
    
    # 今日记录数
    today = date.today()
    today_count = (await db.execute(
        select(func.count(PredictionRecord.id)).where(
            func.date(PredictionRecord.created_at) == today
        )
    )).scalar() or 0
    
    # 健康/病害统计
    healthy_count = (await db.execute(
        select(func.count(PredictionRecord.id)).where(
            PredictionRecord.predicted_class.ilike("%healthy%")
        )
    )).scalar() or 0
    diseased_count = total - healthy_count
    healthy_rate = round(healthy_count / total, 4) if total > 0 else 0
    
    # 按类别统计
    stats_result = await db.execute(
        select(PredictionRecord.predicted_class, func.count(PredictionRecord.id).label("count"))
        .group_by(PredictionRecord.predicted_class)
    )
    class_stats = [{"class": row[0], "count": row[1]} for row in stats_result.all()]
    
    # 按作物统计
    crop_stats = {}
    for item in class_stats:
        crop = item["class"].split("___")[0] if "___" in item["class"] else item["class"]
        if crop not in crop_stats:
            crop_stats[crop] = {"crop": crop, "count": 0, "healthy": 0, "diseased": 0}
        crop_stats[crop]["count"] += item["count"]
        if "healthy" in item["class"].lower():
            crop_stats[crop]["healthy"] += item["count"]
        else:
            crop_stats[crop]["diseased"] += item["count"]
    
    return {
        "total": total,
        "today_count": today_count,
        "healthy_count": healthy_count,
        "diseased_count": diseased_count,
        "healthy_rate": healthy_rate,
        "by_class": class_stats,
        "by_crop": list(crop_stats.values())
    }


@router.get("/stats/trend")
async def get_stats_trend(
    start_date: str = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: str = Query(None, description="结束日期 YYYY-MM-DD"),
    granularity: str = Query("day", description="粒度: day/week/month"),
    db: AsyncSession = Depends(get_db)
):
    """获取趋势统计数据"""
    # 默认30天
    end = date.today() if not end_date else datetime.strptime(end_date, "%Y-%m-%d").date()
    start = end - timedelta(days=30) if not start_date else datetime.strptime(start_date, "%Y-%m-%d").date()
    
    # 查询范围内的记录
    result = await db.execute(
        select(PredictionRecord).where(
            and_(
                func.date(PredictionRecord.created_at) >= start,
                func.date(PredictionRecord.created_at) <= end
            )
        )
    )
    records = result.scalars().all()
    
    # 按日期聚合
    data_map = {}
    for r in records:
        d = r.created_at.date()
        if granularity == "week":
            d = d - timedelta(days=d.weekday())
        elif granularity == "month":
            d = d.replace(day=1)
        key = d.isoformat()
        if key not in data_map:
            data_map[key] = {"date": key, "total": 0, "healthy": 0, "diseased": 0}
        data_map[key]["total"] += 1
        if "healthy" in r.predicted_class.lower():
            data_map[key]["healthy"] += 1
        else:
            data_map[key]["diseased"] += 1
    
    return {"data": sorted(data_map.values(), key=lambda x: x["date"])}