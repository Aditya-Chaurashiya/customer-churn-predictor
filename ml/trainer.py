import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import numpy as np

class ModelTrainer:
    def __init__(self, model, config):
        self.model = model
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
    def train(self, X_train, y_train, X_val, y_val) -> dict:
        batch_size = self.config.get('batch_size', 64)
        epochs = self.config.get('epochs', 100)
        lr = self.config.get('learning_rate', 0.001)
        patience = self.config.get('patience', 10)
        
        X_train_t = torch.FloatTensor(X_train.values if hasattr(X_train, 'values') else X_train)
        y_train_t = torch.FloatTensor(y_train).view(-1, 1)
        X_val_t = torch.FloatTensor(X_val.values if hasattr(X_val, 'values') else X_val)
        y_val_t = torch.FloatTensor(y_val).view(-1, 1)
        
        train_dataset = TensorDataset(X_train_t, y_train_t)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        
        criterion = nn.BCEWithLogitsLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5)
        
        history = {'train_losses': [], 'val_losses': [], 'train_accs': [], 'val_accs': []}
        best_val_loss = float('inf')
        patience_counter = 0
        
        for epoch in range(epochs):
            self.model.train()
            train_loss = 0
            correct = 0
            total = 0
            
            for batch_X, batch_y in train_loader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)
                
                optimizer.zero_grad()
                logits = self.model(batch_X)
                loss = criterion(logits, batch_y)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item() * batch_X.size(0)
                preds = (torch.sigmoid(logits) >= 0.5).float()
                correct += (preds == batch_y).sum().item()
                total += batch_X.size(0)
                
            train_loss /= total
            train_acc = correct / total
            
            self.model.eval()
            with torch.no_grad():
                X_val_dev = X_val_t.to(self.device)
                y_val_dev = y_val_t.to(self.device)
                val_logits = self.model(X_val_dev)
                val_loss = criterion(val_logits, y_val_dev).item()
                val_preds = (torch.sigmoid(val_logits) >= 0.5).float()
                val_acc = (val_preds == y_val_dev).sum().item() / len(y_val_dev)
                
            history['train_losses'].append(train_loss)
            history['val_losses'].append(val_loss)
            history['train_accs'].append(train_acc)
            history['val_accs'].append(val_acc)
            
            scheduler.step(val_loss)
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                patience_counter = 0
                # save best model state implicitly by just keeping the current model
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    print(f"Early stopping at epoch {epoch}")
                    break
                    
        return history
        
    def evaluate(self, X_test, y_test) -> dict:
        self.model.eval()
        X_test_t = torch.FloatTensor(X_test.values if hasattr(X_test, 'values') else X_test).to(self.device)
        
        with torch.no_grad():
            probs = self.model.predict_proba(X_test_t).cpu().numpy().flatten()
            
        preds = (probs >= 0.5).astype(int)
        
        metrics = {
            'accuracy': float(accuracy_score(y_test, preds)),
            'precision': float(precision_score(y_test, preds, zero_division=0)),
            'recall': float(recall_score(y_test, preds, zero_division=0)),
            'f1': float(f1_score(y_test, preds, zero_division=0)),
            'roc_auc': float(roc_auc_score(y_test, probs)),
            'confusion_matrix': confusion_matrix(y_test, preds).tolist(),
            'classification_report': classification_report(y_test, preds, output_dict=True, zero_division=0)
        }
        return metrics
        
    def predict(self, X):
        self.model.eval()
        X_t = torch.FloatTensor(X.values if hasattr(X, 'values') else X).to(self.device)
        with torch.no_grad():
            probs = self.model.predict_proba(X_t).cpu().numpy().flatten()
        preds = (probs >= 0.5).astype(int)
        return preds, probs
        
    def save_model(self, filepath):
        torch.save(self.model.state_dict(), filepath)
        
    @classmethod
    def load_model(cls, filepath, input_dim, config, model_class):
        model = model_class(input_dim, hidden_layers=config.get('hidden_layers', [128, 64, 32]), dropout_rate=config.get('dropout', 0.3))
        model.load_state_dict(torch.load(filepath, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
        return cls(model, config)
