# app/router/predict_router.py
from fastapi import APIRouter, UploadFile, File
from controller.predict_controller import predict_service

router = APIRouter(prefix="/predict", tags=["Food Classification"])

@router.post("")
async def predict_route(file: UploadFile = File(...)):
    return await predict_service(file)
