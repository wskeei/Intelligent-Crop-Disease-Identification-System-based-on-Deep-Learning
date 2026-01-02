# Windows Training Guide (NVIDIA RTX 4060)

This guide explains how to migrate your training to a Windows machine with an NVIDIA GPU.

## 1. Prerequisites

### Install Python & PyTorch
1.  **Install Python 3.10+**: Download from [python.org](https://www.python.org/). Check "Add Python to PATH" during installation.
2.  **Install CUDA Toolkit**: For RTX 4060, install CUDA 11.8 or 12.1 from [NVIDIA Developer](https://developer.nvidia.com/cuda-downloads).
3.  **Install PyTorch**: Open PowerShell or Command Prompt and run the command generated from [pytorch.org](https://pytorch.org/get-started/locally/) for your CUDA version.
    *   *Example (CUDA 12.1)*:
        ```bash
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
        ```

## 2. Project Setup

1.  **Copy Project**: Transfer the entire project folder to your Windows machine.
2.  **Dataset**:
    *   Download the dataset zip: [PlantVillage-Dataset](https://github.com/spMohanty/PlantVillage-Dataset/archive/refs/heads/master.zip)
    *   Extract it.
    *   Create a folder `backend\training\data`.
    *   Move the contents of `PlantVillage-Dataset-master\raw\color` into `backend\training\data`.
    *   Result: You should have folders like `backend\training\data\Tomato___healthy`, etc.

## 3. Running Training

Method A: **Using the Batch Script**
1.  Navigate to `backend\training`.
2.  Double-click `run_training_windows.bat`.

Method B: **Command Line**
1.  Open CMD/PowerShell in the `backend` folder.
2.  Run:
    ```bash
    python training/train_advanced.py --data_dir training/data --epochs 20
    ```

## 4. Verification
The script has been updated to automatically detect:
*   **GPU**: It should say `Using device: cuda`.
*   **Optimization**: It will use `fbgemm` engine for quantization on Windows/Intel/AMD CPUs.

## 5. Deployment
After training, take the generated `quantized_model_scripted.pt` file and copy it back to your Mac (or deployment server) into the `backend/ml_models` folder.
