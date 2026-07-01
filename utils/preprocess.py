import numpy as np

try:
    from tensorflow.keras.applications.resnet import preprocess_input
except Exception as exc:
    preprocess_input = None
    _tensorflow_import_error = exc
else:
    _tensorflow_import_error = None


def preprocess_image(img):
    if preprocess_input is None:
        raise RuntimeError(f"TensorFlow is not available: {_tensorflow_import_error}")

    img = img.resize((224, 224))
    img = np.array(img).astype("float32")
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img
