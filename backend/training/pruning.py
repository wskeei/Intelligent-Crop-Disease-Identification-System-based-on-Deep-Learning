import torch
import torch.nn.utils.prune as prune

def apply_structured_pruning(model, amount=0.2):
    """
    Applies structured pruning to Conv2d layers in the model.
    Prunes 'amount' fraction of output channels (L1 norm).
    """
    print(f"Applying structured pruning (amount={amount})...")
    
    # Iterate over all modules and prune Conv2d layers
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            # Prune output channels based on L1 norm
            prune.ln_structured(module, name='weight', amount=amount, n=1, dim=0)
            
    print("Pruning masks applied.")

def remove_pruning_reparameterization(model):
    """
    Makes the pruning permanent by removing the reparameterization 
    (collapsing mask and weight into a new weight).
    """
    print("Making pruning permanent...")
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Conv2d):
            try:
                prune.remove(module, 'weight')
            except ValueError:
                # If no pruning was applied to this specific layer, skip
                pass
    print("Pruning reparameterization removed.")
