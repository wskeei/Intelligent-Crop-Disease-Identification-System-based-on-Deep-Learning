
import torch
print(f"Supported Engines: {torch.backends.quantized.supported_engines}")
print(f"Current Engine: {torch.backends.quantized.engine}")
