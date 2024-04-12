import torch
import torch.nn as nn


class LSTMClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(LSTMClassifier, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        # out = self.fc(out.view(len(x), -1))
        out = self.fc(out[:, -1, :])
        out = self.sigmoid(out)
        return out

class ModelSerializer:
    @staticmethod
    def save(path, model):
        print(f">>> Model saved in {path}")
        torch.save(model, path)
    
    @staticmethod
    def load(path,cpu_only=False):
        print(f">>> Load Model from {path}")
        if cpu_only:
            return torch.load(path,map_location=torch.device('cpu'))
        return torch.load(path)

class ThresholdClassifier(nn.Module):
    def __init__(self, input_size=1, num_classes=1):
        super(ThresholdClassifier, self).__init__()
        self.fc = nn.Linear(input_size, num_classes)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc(x)
        out = self.sigmoid(out)
        return out
