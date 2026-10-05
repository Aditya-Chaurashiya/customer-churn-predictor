import torch
import torch.nn as nn

class ChurnNet(nn.Module):
    def __init__(self, input_dim, hidden_layers=[128, 64, 32], dropout_rate=0.3):
        super(ChurnNet, self).__init__()
        
        layers = []
        current_dim = input_dim
        
        for hidden_dim in hidden_layers:
            layers.append(nn.Linear(current_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_rate))
            current_dim = hidden_dim
            
        self.feature_extractor = nn.Sequential(*layers)
        self.output_layer = nn.Linear(current_dim, 1)
        
    def forward(self, x):
        features = self.feature_extractor(x)
        logits = self.output_layer(features)
        return logits
        
    def predict_proba(self, x):
        logits = self.forward(x)
        return torch.sigmoid(logits)
