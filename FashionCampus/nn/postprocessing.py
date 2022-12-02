import torch
import numpy

label_name = {
            0: "T-shirt/Top",
            1: "Trouser",
            2: "Pullover",
            3: "Dress",
            4: "Coat", 
            5: "Sandal", 
            6: "Shirt",
            7: "Sneaker",
            8: "Bag",
            9: "Ankle Boot"
            }

def predict(model, y):
    #Push image to model
    y_pred = model(y)

    #Get prediction
    y_pred = torch.argmax(y_pred, dim=1)
    # class_names= a
    a =  y_pred.detach().numpy()[0]
    
    return a
