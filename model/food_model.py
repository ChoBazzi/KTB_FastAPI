# app/model/food_model.py
import tensorflow as tf
from tensorflow.keras.models import load_model
from pathlib import Path

MODEL_PATH = "resnet50_food.h5"
model = load_model(MODEL_PATH)   # global load → cold-start 방지

# Label 불러오기 (label.labels.txt 기반)
LABELS_PATH = Path(__file__).resolve().parent.parent / "label.labels.txt"
with LABELS_PATH.open() as f:
    class_names = [line.strip() for line in f if line.strip()]


def predict_tensor(image_tensor):
    """이미지 Tensor(1,224,224,3) → Top3 결과 반환"""
    pred = model.predict(image_tensor)[0]
    top3 = pred.argsort()[-3:][::-1]

    return [
        {"label": class_names[i], "confidence": float(pred[i])}
        for i in top3
    ]


