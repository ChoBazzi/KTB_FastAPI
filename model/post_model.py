# model/post_model.py

# 임시 더미 데이터 (DB 대체)
_posts = [
    {"id": 1, "title": "Welcome Post", "content": "첫 번째 게시글입니다.", "author": "Alice"},
    {"id": 2, "title": "Second Post", "content": "두 번째 게시글입니다.", "author": "Bob"},
]


def get_posts():
    # 전체 게시글 목록 조회
    return _posts.copy()  # 외부 수정 방지용 복사본


def get_post_by_id(post_id: int):
    # ID로 게시글 조회
    return next((p for p in _posts if p["id"] == post_id), None)


def get_post_by_title(title: str):
    # 제목 비교 시 대소문자/양쪽 공백 무시
    normalized = title.strip().lower()
    return next((p for p in _posts if p["title"].strip().lower() == normalized), None)


def add_post(post: dict):
    # 새 게시글 추가
    _posts.append(post)
    return post


def _find_post(post_id: int):
    # 내부에서만 사용되는 검색 헬퍼
    for post in _posts:
        if post["id"] == post_id:
            return post
    return None


def update_post(post_id: int, data: dict):
    # 게시글 내용 업데이트
    post = _find_post(post_id)
    if post:
        post.update(data)
    return post


def delete_post(post_id: int):
    # 게시글 삭제
    post = _find_post(post_id)
    if post:
        _posts.remove(post)
        return post
    return None
