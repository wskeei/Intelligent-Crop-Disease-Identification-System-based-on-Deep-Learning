# CropVision-AI 后端服务

基于 FastAPI 的农作物病害识别 API 服务。

## 快速开始

### 1. 安装依赖

```bash
# 使用 uv 创建虚拟环境并安装依赖
uv venv --python 3.11
uv sync
```

### 2. 放置模型文件

将 Colab 训练好的模型文件放入 `ml_models/` 目录：
- `best_model.pth` - 模型权重文件
- `class_mapping.json` - 类别映射文件

### 3. 启动服务

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动开发服务器
uvicorn app.main:app --reload
```

服务启动后访问：
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/predict` | 上传图片进行病害识别 |
| GET | `/api/history` | 获取识别历史记录 |
| GET | `/api/stats` | 获取统计数据 |

## 目录结构

```
backend/
├── app/
│   ├── api/          # API 路由
│   ├── core/         # 核心配置
│   ├── models/       # 数据库模型
│   ├── schemas/      # Pydantic 模型
│   └── services/     # 业务逻辑
├── ml_models/        # 模型文件
├── uploads/          # 上传图片
└── pyproject.toml    # 依赖配置