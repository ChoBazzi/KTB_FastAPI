import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from model.post_model import posts as post_model

logger = logging.getLogger(__name__)

async def posts(request: Request, offset: int, limit: int):
    """
    게시글 목록 조회 컨트롤러
    - 쿼리 파라미터를 검증 및 전달
    - 모델 계층을 호출해 실제 데이터를 가져옵니다.
    """
    try:
        request_data = {"offset": offset, "limit": limit}
        response_data = await post_model(request_data)
        logger.info(f"posts Controller: {response_data}")
        return JSONResponse(status_code=200, content=jsonable_encoder(response_data))
    except Exception as e:
        logger.error(f"Error loading posts: {e}")
        return JSONResponse(status_code=500, content={"code": "internal_server_error"})