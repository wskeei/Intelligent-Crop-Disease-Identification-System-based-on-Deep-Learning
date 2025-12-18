# CropVision-AI 🌾

### 基于深度学习的农作物病害智能识别系统

**Intelligent Crop Disease Identification System based on Deep Learning**

## 📖 项目介绍 (Introduction)

**CropVision-AI** 是一个现代化的全栈农作物病害识别系统。本项目旨在利用计算机视觉技术解决农业生产中的病害诊断难题。系统基于 **PlantVillage** 公开数据集，采用深度学习模型（ResNet/EfficientNet）进行特征提取与分类，并通过高性能的 Web 界面为用户提供实时的病害诊断、防治建议及历史记录分析服务。

**主要功能：**

* 🌱 **智能识别**：支持多种农作物（如番茄、马铃薯等）的几十种常见病害识别。
* 📊 **数据可视化**：基于 ECharts 展示识别记录统计与病害分布。
* ⚡ **高性能推理**：基于 FastAPI 异步架构与 ONNX Runtime（可选）加速模型推理。
* 📝 **历史回溯**：完整的识别历史记录存储与查询功能。

---

## 🛠 技术栈 (Tech Stack)

本项目采用前后端分离架构，选取了目前工业界主流且高效的工具链。

### 🐍 后端 & AI (Backend & AI)

* **编程语言**: Python 3.12
* **包管理**: `uv` (极速 Python 包管理器，替代 pip/poetry)
* **Web 框架**: FastAPI (高性能、异步、自动生成文档)
* **深度学习**: PyTorch (模型训练), Torchvision (图像处理)
* **数据库**: SQLite (轻量级存储) + SQLAlchemy (ORM)
* **图像处理**: Pillow, OpenCV

### 💻 前端 (Frontend)

* **核心框架**: Vue 3 (Composition API)
* **语言**: TypeScript (强类型支持)
* **构建工具**: Vite (秒级热更新)
* **UI 组件库**: Element Plus
* **网络请求**: Axios
* **可视化**: ECharts 5

---

## 🗺️ 开发规划 (Roadmap)

本项目开发周期预计分为四个阶段，目前进展如下：

### Phase 1: AI 模型核心 (AI Core)

* [ ] **数据准备**: 下载 PlantVillage 数据集，进行清洗与划分 (Train/Val/Test)。
* [ ] **数据增强**: 实现旋转、裁剪、归一化等预处理脚本。
* [ ] **模型训练**: 搭建 ResNet50/EfficientNet 迁移学习代码。
* [ ] **模型评估**: 输出准确率 (Accuracy) 与混淆矩阵，保存最佳权重文件 (`.pth`)。

### Phase 2: 后端服务开发 (Backend API)

* [ ] **环境搭建**: 使用 `uv` 初始化项目，配置虚拟环境。
* [ ] **API 基础**: 搭建 FastAPI 骨架，配置 CORS 与日志。
* [ ] **模型服务化**: 编写单例加载器，实现图像预测接口 (`POST /api/predict`)。
* [ ] **数据库集成**: 设计 SQLite 表结构，实现历史记录存储接口。

### Phase 3: 前端应用构建 (Frontend UI)

* [ ] **脚手架**: 初始化 Vue3 + TS + Vite 项目。
* [ ] **UI 布局**: 设计侧边栏与顶部导航 (Layout)。
* [ ] **核心功能**: 开发图片上传组件，联调预测接口。
* [ ] **结果展示**: 美化识别结果页，集成 ECharts 数据大屏。

### Phase 4: 部署与优化 (Deployment)

* [ ] **Docker 化**: 编写 `Dockerfile` 与 `docker-compose.yml`。
* [ ] **性能优化**: 尝试将模型导出为 ONNX 格式以加速推理。

---

## 📂 目录结构 (Directory Structure)

```text
CropVision-AI/
├── backend/                # 后端代码
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置 (Config, Security)
│   │   ├── models/         # 数据库模型 (SQLAlchemy)
│   │   ├── schemas/        # Pydantic 数据验证
│   │   ├── services/       # 业务逻辑 (AI 推理, CRUD)
│   │   └── main.py         # 启动入口
│   ├── ml_models/          # 存放训练好的 .pth 模型文件
│   ├── pyproject.toml      # uv 依赖管理
│   └── uploads/            # 图片存储目录
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/            # Axios 请求封装
│   │   ├── components/     # 公共组件
│   │   ├── views/          # 页面视图
│   │   └── App.vue
│   └── package.json
└── notebooks/              # Jupyter Notebooks (用于模型训练与实验)

```

---

## 🚀 快速开始 (Quick Start)

### 后端启动

```bash
cd backend
# 安装依赖
uv sync
# 激活环境并运行
source .venv/bin/activate
uvicorn app.main:app --reload

```

### 前端启动

```bash
cd frontend
# 安装依赖
npm install
# 开发模式运行
npm run dev

```

---

### 💡 下一步建议

这个 README 已经为你搭好了骨架。为了让你能立刻开始动手，**你需要我先帮你生成 `backend` 文件夹下的 `pyproject.toml` 依赖配置文件，还是先帮你写那个“模型训练”的 Python 脚本？**