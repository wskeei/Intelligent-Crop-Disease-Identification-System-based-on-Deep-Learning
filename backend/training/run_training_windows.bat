@echo off
SETLOCAL

REM CropVision-AI Windows Training Helper

echo ===================================================
echo     CropVision-AI Windows Training Launcher
echo ===================================================

REM Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not found in your PATH. 
    echo Please install Python 3.10+ or Anaconda and add it to PATH.
    pause
    exit /b
)

echo.
echo Installing requirements (if needed)...
pip install torch torchvision numpy Pillow tqdm --quiet

echo.
echo Setting up data...
REM Only run if data dir doesn't exist
if not exist "data\plantvillage" (
    echo NOTE: For Windows, due to lack of wget/unzip standard availability, 
    echo Step 1: Please download the PlantVillage dataset manually from:
    echo        https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip
    echo Step 2: Extract it.
    echo Step 3: Move 'raw\color' folder content into 'backend\training\data'
    echo.
    echo If you have already done this and 'data' folder has images, you can ignore this.
)

REM We assume the user runs this from backend/training or root? 
REM Let's assume user runs from root or backend. 
REM Adjusting paths relative to script location.
cd /d "%~dp0"
cd ..

echo.
echo Starting Training on NVIDIA GPU (if available)...
python training/train_advanced.py --data_dir training/data --epochs 20

echo.
echo Training Complete. Model saved in backend folder.
pause
