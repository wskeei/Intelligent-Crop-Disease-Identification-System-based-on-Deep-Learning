
import sys
import torch
from pathlib import Path
from PIL import Image

# Add backend to sys path
backend_path = Path("backend").resolve()
sys.path.append(str(backend_path))

# Setup dummy image
dummy_image_path = Path("dummy_test.jpg")
if not dummy_image_path.exists():
    img = Image.new('RGB', (224, 224), color = 'red')
    img.save(dummy_image_path)

try:
    print(f"Testing Inference with Engine: {torch.backends.quantized.engine}")
    
    from app.services.ai_service import ai_service
    
    # Force reload model just in case (the import instantiates it, so it should have the engine set)
    # Check engine again
    print(f"Current Engine: {torch.backends.quantized.engine}")
    
    print("Model Structure:")
    # print(ai_service._model)
    # Recursively print graph or code
    print(ai_service._model.code)
    
    print("Running prediction...")
    cls, conf, top3 = ai_service.predict(dummy_image_path)
    
    print(f"[SUCCESS] Prediction: {cls} ({conf:.4f})")
    
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    if dummy_image_path.exists():
        try:
            pass # os.remove(dummy_image_path) # Keep for checking
        except:
            pass
