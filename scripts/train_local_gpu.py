import sys
import os
import torch
import time
import subprocess

def run_training():
    print(f"[{time.strftime('%H:%M:%S')}] Initializing Local Training Pipeline...")
    
    # 1. Setup Environment URLs/Paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) # Go up one level from scripts/
    training_path = os.path.join(project_root, 'backend', 'training')
    
    if training_path not in sys.path:
        sys.path.append(training_path)
    
    print(f"Project Root: {project_root}")
    print(f"Training Path: {training_path}")

    # 2. Check Device
    print(f"[{time.strftime('%H:%M:%S')}] Checking Hardware...")
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        total_mem = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"[OK] GPU Detected: {gpu_name}")
        print(f"     VRAM: {total_mem:.2f} GB")
        device = 'cuda'
    else:
        print("[WARNING] GPU NOT Detected. Training will be extremely slow on CPU.")
        device = 'cpu'

    # 3. Configure Training Arguments
    data_dir = os.path.join(training_path, 'data')
    
    # Hyperparameters for RTX 4060
    batch_size = "32" 
    epochs = "20"
    lr = "0.001"
    
    print("\n--- Configuration ---")
    print(f"Data Dir   : {data_dir}")
    print(f"Batch Size : {batch_size}")
    print(f"Epochs     : {epochs}")
    print(f"Try GPU    : {device == 'cuda'}")
    print("---------------------\n")
    
    # Construct command to run train_advanced.py
    # We use subprocess to ensure clean environment and avoiding sys.argv pollution issues if we just imported
    script_path = os.path.join(training_path, 'train_advanced.py')
    
    cmd = [
        sys.executable, script_path,
        "--data_dir", data_dir,
        "--batch_size", batch_size,
        "--epochs", epochs,
        "--lr", lr,
        # Teacher weights: we point to a likely location, but the script handles missing weights gracefully
        "--teacher_weights", os.path.join(project_root, "backend", "ml_models", "best_model.pth")
    ]
    
    print(f"[{time.strftime('%H:%M:%S')}] Launching Training Process...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Run and stream output
        process = subprocess.Popen(cmd, cwd=training_path)
        process.wait()
        
        if process.returncode == 0:
            print(f"\n[{time.strftime('%H:%M:%S')}] \u2705 Training Pipeline Run Successfully!")
            print(f"Check {training_path}/runs for plots and {training_path} for saved models.")
        else:
            print(f"\n[{time.strftime('%H:%M:%S')}] \u274c Training Pipeline Failed with exit code {process.returncode}.")
            
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user.")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nPress Enter to exit...")
    input()

if __name__ == "__main__":
    run_training()
