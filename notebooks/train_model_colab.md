{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🌾 CropVision-AI 模型训练\n",
    "## 基于 PlantVillage 数据集的农作物病害识别模型\n",
    "\n",
    "本 Notebook 用于在 Google Colab 上训练 ResNet50 迁移学习模型。"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. 环境配置"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 检查 GPU\n",
    "!nvidia-smi"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import torch\n",
    "import torch.nn as nn\n",
    "import torch.optim as optim\n",
    "from torch.utils.data import DataLoader\n",
    "from torchvision import datasets, transforms, models\n",
    "import os\n",
    "from pathlib import Path\n",
    "\n",
    "device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')\n",
    "print(f'Using device: {device}')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. 下载 PlantVillage 数据集"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 从 Kaggle 下载数据集 (需要先配置 Kaggle API)\n",
    "# 方法1: 使用 kaggle API\n",
    "# !pip install kaggle\n",
    "# !kaggle datasets download -d emmarex/plantdisease\n",
    "\n",
    "# 方法2: 直接从 GitHub 镜像下载\n",
    "!wget -q https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip -O plantvillage.zip\n",
    "!unzip -q plantvillage.zip\n",
    "!mv PlantVillage-Dataset-master/raw/color ./data\n",
    "!rm -rf PlantVillage-Dataset-master plantvillage.zip"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 查看数据集类别\n",
    "data_dir = Path('./data')\n",
    "classes = sorted([d.name for d in data_dir.iterdir() if d.is_dir()])\n",
    "num_classes = len(classes)\n",
    "print(f'类别数量: {num_classes}')\n",
    "print(f'类别列表: {classes[:5]}...')  # 显示前5个"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. 数据预处理与增强"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 数据增强\n",
    "train_transform = transforms.Compose([\n",
    "    transforms.RandomResizedCrop(224),\n",
    "    transforms.RandomHorizontalFlip(),\n",
    "    transforms.RandomRotation(15),\n",
    "    transforms.ColorJitter(brightness=0.2, contrast=0.2),\n",
    "    transforms.ToTensor(),\n",
    "    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])\n",
    "])\n",
    "\n",
    "val_transform = transforms.Compose([\n",
    "    transforms.Resize(256),\n",
    "    transforms.CenterCrop(224),\n",
    "    transforms.ToTensor(),\n",
    "    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])\n",
    "])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 划分数据集 (80% 训练, 20% 验证)\n",
    "from torch.utils.data import random_split\n",
    "\n",
    "full_dataset = datasets.ImageFolder(data_dir, transform=train_transform)\n",
    "train_size = int(0.8 * len(full_dataset))\n",
    "val_size = len(full_dataset) - train_size\n",
    "\n",
    "train_dataset, val_dataset = random_split(full_dataset, [train_size, val_size])\n",
    "val_dataset.dataset.transform = val_transform  # 验证集使用不同的transform\n",
    "\n",
    "print(f'训练集: {train_size}, 验证集: {val_size}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 创建 DataLoader\n",
    "BATCH_SIZE = 32\n",
    "\n",
    "train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)\n",
    "val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. 构建 ResNet50 迁移学习模型"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 加载预训练 ResNet50\n",
    "model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)\n",
    "\n",
    "# 冻结特征提取层\n",
    "for param in model.parameters():\n",
    "    param.requires_grad = False\n",
    "\n",
    "# 替换分类头\n",
    "model.fc = nn.Sequential(\n",
    "    nn.Dropout(0.5),\n",
    "    nn.Linear(model.fc.in_features, num_classes)\n",
    ")\n",
    "\n",
    "model = model.to(device)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 损失函数和优化器\n",
    "criterion = nn.CrossEntropyLoss()\n",
    "optimizer = optim.Adam(model.fc.parameters(), lr=0.001)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. 训练模型"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def train_epoch(model, loader, criterion, optimizer):\n",
    "    model.train()\n",
    "    running_loss, correct, total = 0.0, 0, 0\n",
    "    \n",
    "    for images, labels in loader:\n",
    "        images, labels = images.to(device), labels.to(device)\n",
    "        \n",
    "        optimizer.zero_grad()\n",
    "        outputs = model(images)\n",
    "        loss = criterion(outputs, labels)\n",
    "        loss.backward()\n",
    "        optimizer.step()\n",
    "        \n",
    "        running_loss += loss.item()\n",
    "        _, predicted = outputs.max(1)\n",
    "        total += labels.size(0)\n",
    "        correct += predicted.eq(labels).sum().item()\n",
    "    \n",
    "    return running_loss / len(loader), 100. * correct / total\n",
    "\n",
    "def validate(model, loader, criterion):\n",
    "    model.eval()\n",
    "    running_loss, correct, total = 0.0, 0, 0\n",
    "    \n",
    "    with torch.no_grad():\n",
    "        for images, labels in loader:\n",
    "            images, labels = images.to(device), labels.to(device)\n",
    "            outputs = model(images)\n",
    "            loss = criterion(outputs, labels)\n",
    "            \n",
    "            running_loss += loss.item()\n",
    "            _, predicted = outputs.max(1)\n",
    "            total += labels.size(0)\n",
    "            correct += predicted.eq(labels).sum().item()\n",
    "    \n",
    "    return running_loss / len(loader), 100. * correct / total"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 训练循环\n",
    "EPOCHS = 10\n",
    "best_acc = 0.0\n",
    "\n",
    "for epoch in range(EPOCHS):\n",
    "    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer)\n",
    "    val_loss, val_acc = validate(model, val_loader, criterion)\n",
    "    \n",
    "    print(f'Epoch [{epoch+1}/{EPOCHS}] '\n",
    "          f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% | '\n",
    "          f'Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')\n",
    "    \n",
    "    # 保存最佳模型\n",
    "    if val_acc > best_acc:\n",
    "        best_acc = val_acc\n",
    "        torch.save({\n",
    "            'model_state_dict': model.state_dict(),\n",
    "            'classes': classes,\n",
    "            'num_classes': num_classes\n",
    "        }, 'best_model.pth')\n",
    "        print(f'  -> 保存最佳模型 (Acc: {best_acc:.2f}%)')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. 模型评估"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.metrics import classification_report, confusion_matrix\n",
    "import numpy as np\n",
    "\n",
    "# 加载最佳模型\n",
    "checkpoint = torch.load('best_model.pth')\n",
    "model.load_state_dict(checkpoint['model_state_dict'])\n",
    "\n",
    "# 收集预测结果\n",
    "model.eval()\n",
    "all_preds, all_labels = [], []\n",
    "\n",
    "with torch.no_grad():\n",
    "    for images, labels in val_loader:\n",
    "        images = images.to(device)\n",
    "        outputs = model(images)\n",
    "        _, preds = outputs.max(1)\n",
    "        all_preds.extend(preds.cpu().numpy())\n",
    "        all_labels.extend(labels.numpy())\n",
    "\n",
    "print(f'最终验证准确率: {best_acc:.2f}%')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7. 下载模型到本地"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 在 Colab 中下载模型文件\n",
    "from google.colab import files\n",
    "files.download('best_model.pth')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 保存类别映射 (用于后端推理)\n",
    "import json\n",
    "\n",
    "class_mapping = {i: name for i, name in enumerate(classes)}\n",
    "with open('class_mapping.json', 'w') as f:\n",
    "    json.dump(class_mapping, f, indent=2)\n",
    "\n",
    "files.download('class_mapping.json')"
   ]
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {
   "gpuType": "T4",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}