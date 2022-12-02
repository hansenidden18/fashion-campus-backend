from .preprocessing import normalize_image
from .inference import extract_model
from .postprocessing import predict

#input path
#path = base64

def predict_image(path):
    img = normalize_image(path)
    model = extract_model()
    
    return predict(model, img)
    