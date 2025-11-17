from fastapi import APIRouter, Query, Request
from controller.post_controller import posts

router = APIRouter()

@router.get("/posts")
async def posts_endpoint(
    request: Request,
    offset: int = Query(0, ge=0, description="조회 시작 위치 (기본값 0)"),
    limit: int = Query(10, le=50, description="조회 개수 (최대 50)"),
):
    """
    게시글 목록 조회 엔드포인트
    - GET /posts?offset=0&limit=10
    - 게시글 목록을 페이징 단위로 조회합니다.
    """
    return await posts(request, offset, limit)