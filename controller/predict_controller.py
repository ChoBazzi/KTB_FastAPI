# app/controller/predict_controller.py
from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
import io

from utils.preprocess import preprocess_image
from model.food_model import ModelNotReadyError, get_model_status, predict_tensor


async def predict_service(file: UploadFile):
    """업로드 받은 파일을 이미지 → Tensor 변환 후 모델 예측"""
    img_bytes = await file.read()
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise HTTPException(status_code=400, detail="invalid_image_file") from exc

    try:
        tensor = preprocess_image(img)
        result = predict_tensor(tensor)
    except ModelNotReadyError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return {"top3": result}


def model_health_service():
    """모델 파일/라벨 준비 상태 확인용 엔드포인트"""
    return get_model_status()
