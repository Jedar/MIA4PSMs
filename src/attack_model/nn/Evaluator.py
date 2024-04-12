from typing import Any
import torch
import torch.nn as nn
from dataclasses import dataclass

from Dataset import *
from Model import *
from Metrics import *

@dataclass
class EvaluatorConfig:
    batch_size: int = 32
    model_load: str = ""
    dict_size: int = 10
    max_len: int = 12

class Evaluator:
    def __init__(self, config, device, cpu_only=False):
        self.model = ModelSerializer.load(config.model_load,cpu_only)
        self.model.eval()
        self.config = config
        self.device = device
    
    def infer(self, data):
        return self.model(data.to(self.device)).squeeze().detach().round().cpu()
    
    def __call__(self, data):
        data = data.unsqueeze(0)
        return self.infer(data)

class BatchEvaluator(Evaluator):
    def __init__(self, config, device):
        super().__init__(config, device)
        self.batch_size = config.batch_size
    
    def __call__(self, data):
        if len(data.shape) <= 2:
            data = data.unsqueeze(0)
        return self.infer(data)

class BatchDirectEvaluator(BatchEvaluator):
    def __init__(self, config, device):
        super().__init__(config, device)
    
    def infer(self, data):
        return self.model(data.to(self.device)).squeeze().detach().cpu()
