
import sys
from pathlib import Path

# Add backend to sys path to simulate running from backend dir
backend_path = Path("backend").resolve()
sys.path.append(str(backend_path))

from app.services.ai_service import ai_service as aiservice

try:
    print(f"Checking Model Loading...")
    model = aiservice._model
    if model is None:
        print("[ERROR] Model is None!")
        sys.exit(1)
        
    print(f"[SUCCESS] Model loaded: {type(model)}")
    
    if hasattr(model, 'code'): # Check if it is a scripted/JIT model
         print("[INFO] Model is TorchScript/JIT.")
    else:
         print("[INFO] Model is Standard PyTorch Module.")

except Exception as e:
    print(f"[ERROR] Failed to verify model: {e}")
    sys.exit(1)
