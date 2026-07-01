# app/router/predict_router.py
from fastapi import APIRouter, UploadFile, File
from controller.predict_controller import model_health_service, predict_service

router = APIRouter(prefix="/predict", tags=["Food Classification"])


@router.get("/health")
def model_health_route():
    return model_health_service()


@router.post("")
async def predict_route(file: UploadFile = File(...)):
    return await predict_service(file)
