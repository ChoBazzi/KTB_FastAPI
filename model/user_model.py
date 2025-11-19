# models/user_model.py

# 임시 더미 데이터 (DB 대체)
_users = [
    {"id": 1, "name": "Alice", "email": "alice@test.com", "password": "alice123"},
    {"id": 2, "name": "Bob", "email": "bob@test.com", "password": "bob123"},
    {"id": 3, "name": "Carol", "email": "carol@test.com", "password": "carol123"},
]

# 모든 사용자 조회
def get_users():
    return _users.copy()  # 외부에서 수정 방지

# ID로 사용자 조회
def get_user_by_id(user_id: int):
    return next((u for u in _users if u["id"] == user_id), None)

# 이메일로 사용자 조회
def get_user_by_email(email: str):
    return next((u for u in _users if u["email"] == email), None)

# 새 사용자 추가
def add_user(user: dict):
    _users.append(user)
    return user

# 사용자 정보 업데이트용 회원검색 함수
def upd_user_by_id(user_id: int):
    for u in _users:
        if u["id"] == user_id:
            return u  # ✅ 원본 dict 반환
    return None

# 회원 정보 수정
def update_user(user_id: int, data: dict):
    user = upd_user_by_id(user_id)
    if user:
        user.update(data)
    return user

# 비밀번호 변경
def password_update_user(user_id: int, data: dict):
    user = upd_user_by_id(user_id)
    if user:
        user.update(data)
    return user

# 회원 삭제 
def delete_user(user_id: int):
    user = upd_user_by_id(user_id)
    if user:
        _users.remove(user)
        return user
    return None