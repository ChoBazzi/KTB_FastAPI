from pathlib import Path

from config import settings


class ModelNotReadyError(RuntimeError):
    """Raised when the prediction model cannot be loaded."""


MODEL_PATH = Path(settings.model_path).expanduser()
if not MODEL_PATH.is_absolute():
    MODEL_PATH = Path(__file__).resolve().parent.parent / MODEL_PATH

LABELS_PATH = Path(__file__).resolve().parent.parent / "label.labels.txt"
with LABELS_PATH.open() as f:
    class_names = [line.strip() for line in f if line.strip()]

_model = None
_load_error = None


def _load_model():
    """Load the Keras model on first prediction instead of at API import time."""
    global _model, _load_error

    if _model is not None:
        return _model
    if _load_error is not None:
        raise ModelNotReadyError(_load_error)
    if not MODEL_PATH.exists():
        _load_error = f"model file not found: {MODEL_PATH}"
        raise ModelNotReadyError(_load_error)

    try:
        from tensorflow.keras.models import load_model

        _model = load_model(MODEL_PATH)
        return _model
    except Exception as exc:
        _load_error = f"failed to load model: {exc}"
        raise ModelNotReadyError(_load_error) from exc


def get_model_status():
    return {
        "ready": _model is not None,
        "model_path": str(MODEL_PATH),
        "model_exists": MODEL_PATH.exists(),
        "labels_count": len(class_names),
        "load_error": _load_error,
    }


def predict_tensor(image_tensor):
    """이미지 Tensor(1,224,224,3) → Top3 결과 반환"""
    model = _load_model()
    pred = model.predict(image_tensor, verbose=0)[0]
    if len(pred) != len(class_names):
        raise ModelNotReadyError(
            f"model output size({len(pred)}) does not match labels({len(class_names)})"
        )

    top3 = pred.argsort()[-3:][::-1]

    return [
        {"label": class_names[i], "confidence": float(pred[i])}
        for i in top3
    ]
