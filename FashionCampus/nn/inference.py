from .model import CNNModel
import torch
from os.path import join, dirname, realpath

def extract_model():
    model = CNNModel()
    PATH = join(dirname(realpath(__file__)), "cnnmodel1.pt")
    model.load_state_dict(torch.load(PATH))

    return model