from .model import CNNModel
import torch

def extract_model():
    model = CNNModel()
    PATH = "cnnmodel1.pt"
    model.load_state_dict(torch.load(PATH))

    return model