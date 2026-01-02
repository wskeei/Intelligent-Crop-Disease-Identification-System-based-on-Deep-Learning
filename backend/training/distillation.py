import torch
import torch.nn as nn
import torch.nn.functional as F

class KnowledgeDistillationLoss(nn.Module):
    """
    Knowledge Distillation Loss
    Combines strict CrossEntropyLoss (student vs true labels) 
    and KLDivLoss (student logits vs teacher logits).
    """
    def __init__(self, alpha=0.5, temperature=3.0):
        super(KnowledgeDistillationLoss, self).__init__()
        self.alpha = alpha
        self.temperature = temperature
        self.criterion_ce = nn.CrossEntropyLoss()
        self.criterion_kl = nn.KLDivLoss(reduction='batchmean')

    def forward(self, student_logits, teacher_logits, labels):
        # Softmax for teacher and student with temperature
        teacher_probs = F.softmax(teacher_logits / self.temperature, dim=1)
        student_log_probs = F.log_softmax(student_logits / self.temperature, dim=1)
        
        # KD Loss: KL Divergence between softened distributions
        loss_kd = self.criterion_kl(student_log_probs, teacher_probs) * (self.temperature ** 2)
        
        # Standard Cross Entropy Loss
        loss_ce = self.criterion_ce(student_logits, labels)
        
        # Combine
        total_loss = self.alpha * loss_kd + (1 - self.alpha) * loss_ce
        return total_loss
