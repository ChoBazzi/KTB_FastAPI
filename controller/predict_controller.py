# app/controller/predict_controller.py
from fastapi import UploadFile
from PIL import Image
import io

from utils.preprocess import preprocess_image
from model.food_model import predict_tensor


async def predict_service(file: UploadFile):
    """업로드 받은 파일을 이미지 → Tensor 변환 후 모델 예측"""
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

    tensor = preprocess_image(img)
    result = predict_tensor(tensor)

    return {"top3": result}
