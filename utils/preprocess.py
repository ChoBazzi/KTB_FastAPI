from tensorflow.keras.applications.resnet import preprocess_input
import numpy as np
from PIL import Image

def preprocess_image(img):
    img = img.resize((224, 224))
    img = np.array(img).astype("float32")
    img = preprocess_input(img)       # 🔥 핵심
    img = np.expand_dims(img, axis=0)
    return img