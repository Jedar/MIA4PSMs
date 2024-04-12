import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from dataclasses import dataclass

from Dataset import *
from Model import *
from Metrics import *


@dataclass
class TrainerConfig:
    batch_size: int = 32
    lr: float = 0.001
    num_worker: int = 2
    epochs: int = 10
    model_save: str = ""

class Trainer:
    def __init__(self, model, dataset, config, device):
        self.model = model 
        self.config = config
        self.loss_fn = nn.BCELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=config.lr)
        self.dataloader = dataloader_wrapper(dataset, batch_size=config.batch_size)
        self.device = device

    def train(self):
        self.model.train()
        for i in range(self.config.epochs):
            total_loss = 0
            for seq, labels in self.dataloader:
                seq = seq.to(self.device)
                labels = labels.to(self.device)
                self.optimizer.zero_grad()
                y_pred = self.model(seq).squeeze()
                loss = self.loss_fn(y_pred, labels)
                loss.backward()
                self.optimizer.step()
                total_loss += loss
            print(f"Train epoch {i}: Loss {total_loss}")
        ModelSerializer.save(self.config.model_save, self.model)
    
    def eval(self):
        return self.query(self.dataloader)
        
    def query(self, data):
        self.model.eval()
        total_labels = []
        total_preds = []
        for seq, labels in data:
            seq = seq.to(self.device)
            total_labels += labels
            y_pred = self.model(seq).squeeze().detach()
            total_preds += y_pred.round().cpu()
        print(validate(total_preds, total_labels))

"""
自定义focal loss
focal_loss func, L = -α(1-yi)**γ *ce_loss(xi,yi)
alpha是正样本比例，一般取0.25
gamma降低负样本的Loss比重，一般取2
"""
class FocalLoss(nn.Module):
    def __init__(self, gamma=2, alpha=1):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.alpha = alpha

    def forward(self, inputs, targets):
        ce_loss = F.binary_cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss
        return torch.mean(focal_loss * self.alpha)

class FocusLossTrainer(Trainer):
    def __init__(self, model, dataset, config, device):
        super().__init__(model, dataset, config, device)
        # Focal Loss 默认配置
        self.loss_fn = FocalLoss(gamma=2, alpha=0.25)
