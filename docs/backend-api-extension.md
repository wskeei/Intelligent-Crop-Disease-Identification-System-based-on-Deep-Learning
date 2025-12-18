# CropVision-AI 后端 API 扩展需求

> 版本: v1.0  
> 更新日期: 2024-12-18  
> 状态: 待开发

---

## 一、现有 API 概览

| 接口 | 方法 | 描述 | 状态 |
|------|------|------|------|
| `POST /api/predict` | POST | 上传图片进行病害识别 | ✅ 已实现 |
| `GET /api/history` | GET | 获取识别历史列表 | ✅ 已实现 |
| `GET /api/stats` | GET | 获取统计数据 | ✅ 已实现 |

---

## 二、需要新增/修改的 API

### 2.1 增强预测接口 (P0 - 必须)

**修改现有接口**: `POST /api/predict`

**变更说明**: 返回 Top-3 预测结果，而不仅仅是最高置信度的结果

**当前响应**:
```json
{
  "predicted_class": "Tomato___Early_blight",
  "confidence": 0.856,
  "image_url": "/uploads/xxx.jpg"
}
```

**新响应格式**:
```json
{
  "predicted_class": "Tomato___Early_blight",
  "confidence": 0.856,
  "image_url": "/uploads/xxx.jpg",
  "top_predictions": [
    {"class": "Tomato___Early_blight", "confidence": 0.856},
    {"class": "Tomato___Late_blight", "confidence": 0.082},
    {"class": "Tomato___Leaf_Mold", "confidence": 0.031}
  ]
}
```

**实现要点**:
- 修改 `ai_service.py` 中的 `predict()` 方法，返回 Top-3 结果
- 修改 `PredictionResponse` schema，添加 `top_predictions` 字段
- 数据库可选择是否存储 Top-3 结果

---

### 2.2 历史记录详情接口 (P1)

**新增接口**: `GET /api/history/{id}`

**描述**: 获取单条识别记录的详细信息

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | int | 是 | 记录 ID |

**响应**:
```json
{
  "id": 1,
  "image_path": "abc123.jpg",
  "predicted_class": "Tomato___Early_blight",
  "confidence": 0.856,
  "created_at": "2024-12-18T10:30:00Z"
}
```

**错误响应**:
- 404: 记录不存在

---

### 2.3 删除历史记录接口 (P1)

**新增接口**: `DELETE /api/history/{id}`

**描述**: 删除单条识别记录

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | int | 是 | 记录 ID |

**响应**:
```json
{
  "success": true,
  "message": "删除成功"
}
```

**错误响应**:
- 404: 记录不存在

**实现要点**:
- 删除数据库记录
- 可选: 同时删除对应的图片文件

---

### 2.4 批量删除历史记录接口 (P1)

**新增接口**: `DELETE /api/history/batch`

**描述**: 批量删除多条识别记录

**请求体**:
```json
{
  "ids": [1, 2, 3, 5, 8]
}
```

**响应**:
```json
{
  "success": true,
  "deleted_count": 5
}
```

**实现要点**:
- 使用事务确保原子性
- 返回实际删除的数量（部分 ID 可能不存在）

---

### 2.5 趋势统计接口 (P1)

**新增接口**: `GET /api/stats/trend`

**描述**: 获取按时间维度的统计趋势数据，用于折线图展示

**查询参数**:
| 参数 | 类型 | 必填 | 默认值 | 描述 |
|------|------|------|--------|------|
| start_date | string | 否 | 30天前 | 开始日期 (YYYY-MM-DD) |
| end_date | string | 否 | 今天 | 结束日期 (YYYY-MM-DD) |
| granularity | string | 否 | day | 粒度: day/week/month |

**响应**:
```json
{
  "data": [
    {
      "date": "2024-12-01",
      "total": 15,
      "healthy": 8,
      "diseased": 7
    },
    {
      "date": "2024-12-02",
      "total": 23,
      "healthy": 12,
      "diseased": 11
    }
  ]
}
```

**实现要点**:
- 使用 SQL 的 `DATE()` 函数按日期分组
- 根据 `predicted_class` 是否包含 `healthy` 判断健康/病害
- 支持按周/月聚合

---

### 2.6 增强统计接口 (P1)

**修改现有接口**: `GET /api/stats`

**变更说明**: 增加更多统计维度

**当前响应**:
```json
{
  "total": 100,
  "by_class": [
    {"class": "Tomato___Early_blight", "count": 25}
  ]
}
```

**新响应格式**:
```json
{
  "total": 100,
  "today_count": 15,
  "healthy_count": 40,
  "diseased_count": 60,
  "healthy_rate": 0.4,
  "by_class": [
    {"class": "Tomato___Early_blight", "count": 25}
  ],
  "by_crop": [
    {"crop": "Tomato", "count": 45, "healthy": 10, "diseased": 35}
  ]
}
```

---

### 2.7 病害知识库列表接口 (P2)

**新增接口**: `GET /api/diseases`

**描述**: 获取病害知识库列表

**查询参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| crop | string | 否 | 按作物类型筛选 |

**响应**:
```json
{
  "data": [
    {
      "id": "tomato_early_blight",
      "name_cn": "番茄早疫病",
      "name_en": "Tomato Early Blight",
      "crop": "Tomato",
      "crop_cn": "番茄",
      "is_healthy": false,
      "description": "叶片上出现圆形或近圆形褐色病斑，具有明显的同心轮纹...",
      "image_url": "/static/diseases/tomato_early_blight.jpg"
    }
  ],
  "crops": [
    {"id": "Tomato", "name_cn": "番茄", "count": 10},
    {"id": "Apple", "name_cn": "苹果", "count": 4}
  ]
}
```

**实现要点**:
- 数据可以存储在 JSON 文件中，无需数据库
- 基于 `class_mapping.json` 生成基础数据
- 需要准备中文翻译映射

---

### 2.8 病害详情接口 (P2)

**新增接口**: `GET /api/diseases/{id}`

**描述**: 获取单个病害的详细信息

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | string | 是 | 病害 ID (如 tomato_early_blight) |

**响应**:
```json
{
  "id": "tomato_early_blight",
  "name_cn": "番茄早疫病",
  "name_en": "Tomato Early Blight",
  "crop": "Tomato",
  "crop_cn": "番茄",
  "is_healthy": false,
  "pathogen": "茄链格孢菌 (Alternaria solani)",
  "affected_parts": ["叶片", "茎", "果实"],
  "symptoms": "叶片上出现圆形或近圆形褐色病斑，具有明显的同心轮纹，病斑边缘有黄色晕圈。严重时病斑连片，导致叶片枯死。",
  "conditions": {
    "temperature": "20-25°C",
    "humidity": "高湿环境 (相对湿度 > 80%)",
    "other": ["连作地块", "氮肥过多", "植株衰弱"]
  },
  "prevention": {
    "agricultural": [
      "选用抗病品种",
      "实行 2-3 年轮作",
      "及时清除病残体",
      "合理密植，改善通风"
    ],
    "chemical": [
      {
        "name": "百菌清",
        "concentration": "75% WP 600倍液",
        "method": "叶面喷雾",
        "interval": "7-10天一次"
      },
      {
        "name": "代森锰锌",
        "concentration": "80% WP 500倍液",
        "method": "叶面喷雾",
        "interval": "7天一次"
      }
    ]
  },
  "images": [
    "/static/diseases/tomato_early_blight_1.jpg",
    "/static/diseases/tomato_early_blight_2.jpg"
  ]
}
```

**错误响应**:
- 404: 病害不存在

---

## 三、数据模型变更

### 3.1 PredictionRecord 模型 (可选扩展)

如果需要存储 Top-3 预测结果，可以添加字段:

```python
class PredictionRecord(Base):
    __tablename__ = "prediction_records"
    
    id = Column(Integer, primary_key=True)
    image_path = Column(String, nullable=False)
    predicted_class = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    # 新增字段
    top_predictions = Column(JSON, nullable=True)  # 存储 Top-3 JSON
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 3.2 病害知识库数据结构

建议创建 `backend/data/diseases.json`:

```json
{
  "diseases": [
    {
      "id": "tomato_early_blight",
      "class_name": "Tomato___Early_blight",
      "name_cn": "番茄早疫病",
      "name_en": "Tomato Early Blight",
      "crop": "Tomato",
      "crop_cn": "番茄",
      "is_healthy": false,
      "description": "...",
      "pathogen": "...",
      "symptoms": "...",
      "prevention": {}
    }
  ],
  "crops": [
    {"id": "Tomato", "name_cn": "番茄", "emoji": "🍅"},
    {"id": "Apple", "name_cn": "苹果", "emoji": "🍎"}
  ]
}
```

---

## 四、开发任务清单

| 序号 | 任务 | 优先级 | 预估工时 | 依赖 |
|------|------|--------|----------|------|
| B1 | 增强预测接口 (返回 Top-3) | P0 | 2h | - |
| B2 | 历史记录详情接口 | P1 | 1h | - |
| B3 | 删除历史记录接口 | P1 | 1h | - |
| B4 | 批量删除接口 | P1 | 1h | B3 |
| B5 | 趋势统计接口 | P1 | 3h | - |
| B6 | 增强统计接口 | P1 | 2h | - |
| B7 | 病害知识库数据准备 | P2 | 4h | - |
| B8 | 病害知识库列表接口 | P2 | 2h | B7 |
| B9 | 病害详情接口 | P2 | 1h | B7 |

**总预估工时**: 17h

---

## 五、API 文档更新

完成开发后，FastAPI 会自动生成 Swagger 文档:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

*文档结束*