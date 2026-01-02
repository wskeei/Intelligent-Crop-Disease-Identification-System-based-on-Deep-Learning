import torch
import torch.quantization
from torch.ao.quantization import QuantStub, DeQuantStub

def prepare_model_for_qat(model):
    """
    Prepares the MobileNetV3 model for Quantization Aware Training (QAT).
    """
    print("Preparing model for QAT...")
    
    # MobileNetV3 is Quantization-Ready in torchvision, 
    # but we need to ensure the configuration is correct for QAT.
    
    # 1. Fuse modules (Conv+BN+ReLU is common)
    # MobileNetV3 implementation in torchvision usually has fused modules within its blocks,
    # Detect engine
    engine = torch.backends.quantized.engine
    if engine is None:
        # Fallback based on arch if not set for some reason
        import platform
        if 'arm' in platform.machine().lower():
             engine = 'qnnpack'
        else:
             engine = 'fbgemm'
            
    model.qconfig = torch.ao.quantization.get_default_qat_qconfig(engine)
    
    # 2. Prepare for QAT (inserts observers and fake quant modules)
    # create_qat_model helps, but since we are modifying an existing float model instance:
    torch.ao.quantization.prepare_qat(model, inplace=True)
    
    print("Model prepared for QAT.")
    return model

def convert_qat_model(model):
    """
    Converts a QAT model to a fully quantized model (INT8).
    """
    print("Converting QAT model to INT8...")
    model.eval()
    quantized_model = torch.ao.quantization.convert(model, inplace=False)
    print("Model conversion complete.")
    return quantized_model
