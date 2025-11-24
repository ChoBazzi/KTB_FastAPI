# controller/post_controller.py
from fastapi import HTTPException
from model import post_model


def get_posts():
    # 전체 게시글 목록 반환 (없으면 404)
    posts = post_model.get_posts()
    if not posts:
        raise HTTPException(status_code=404, detail="no_posts_found")
    return {"data": posts}


def get_post(post_id: int):
    # ID로 단일 게시글 조회
    if post_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_post_id")

    post = post_model.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post_not_found")
    return {"data": post}


def create_post(data: dict):
    # 게시글 생성 (제목 중복, 공백 필드 차단)
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    author = (data.get("author") or "anonymous").strip() or "anonymous"

    # 필수값 누락/공백만 입력 방지
    if not title or not content:
        raise HTTPException(status_code=400, detail="missing_required_fields")

    # 제목 중복 방지
    if post_model.get_post_by_title(title):
        raise HTTPException(status_code=409, detail="title_already_exists")

    new_post = {
        "id": len(post_model.get_posts()) + 1,
        "title": title,
        "content": content,
        "author": author,
    }
    post_model.add_post(new_post)
    return {"data": new_post}


def update_post(post_id: int, data: dict):
    # 게시글 수정 (유효성 검증 및 제목 중복 방지)
    if post_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_post_id")

    # None 값만 넘어온 경우 업데이트 불가
    update_data = {k: v for k, v in data.items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="no_fields_to_update")

    # 공백만 있는 필드 예외 처리
    for key in ["title", "content", "author"]:
        if key in update_data and isinstance(update_data[key], str):
            stripped = update_data[key].strip()
            if not stripped:
                raise HTTPException(status_code=400, detail="empty_fields")
            update_data[key] = stripped

    # 제목 중복 체크 (본인 제외)
    if "title" in update_data:
        existing = post_model.get_post_by_title(update_data["title"])
        if existing and existing["id"] != post_id:
            raise HTTPException(status_code=409, detail="title_already_exists")

    post = post_model.update_post(post_id, update_data)
    if not post:
        raise HTTPException(status_code=404, detail="post_not_found")
    return {"data": post}


def delete_post(post_id: int):
    # 게시글 삭제
    if post_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_post_id")

    post = post_model.delete_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post_not_found")
    return {"data": post}
