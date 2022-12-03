from io import BytesIO
from PIL import Image

import numpy as np
import base64
import torch

IMAGE_SHAPE = (28, 28) 

def normalize_image(file_base64):
    # decoding base64
    base_64_decoded = base64.b64decode(file_base64)
    bytes_image = BytesIO(base_64_decoded)
    file = Image.open(bytes_image)
    # file = Image.open(file_base64)

    # greyscaling & resizing
    file = file.convert('L').resize(IMAGE_SHAPE)
    
    # Prepare image for model
    img = np.array(file)
    
    img = np.expand_dims(img, axis=0)
    g = (img / 255.0).astype(np.float32)
    g = np.expand_dims(g, axis=0)
    y = torch.from_numpy(g)
    
    return y 