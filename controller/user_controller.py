# controllers/user_controller.py
from fastapi import HTTPException
from model import user_model

# 사용자 목록 조회
def get_users():
    users = user_model.get_users()
    if not users:
        raise HTTPException(status_code=404, detail="no_users_found")
    return {"data": users}

# 특정 사용자 상세 조회
def get_user(user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_user_id")

    user = user_model.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")

    return {"data": user}

# 사용자 생성
# 패스워드 추가 - 암호화작업x
def create_user(data: dict):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="missing_required_fields")

    if user_model.get_user_by_email(email):
        raise HTTPException(status_code=409, detail="email_already_exists")

    new_user = {"id": len(user_model.get_users()) + 1, "name": name, "email": email, "password": password}
    user_model.add_user(new_user)
    return {"data": new_user}

# 로그인
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="missing_email or password")

    user = user_model.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="unauthorized")

    return {"data": {"user_id": user["id"], "name": user["name"]}}

# 회원정보 수정
def update_user(user_id: int, data: dict):

    email = data.get("email")
    name = data.get("name")

    if not name:
        raise HTTPException(status_code=400, detail="missing_required_fields")
    
    user = user_model.update_user(user_id, data)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    return {"data": user}

# 비밀번호 변경
def password_update_user(user_id: int, data: dict):

    password = data.get("password")

    if not password:
        raise HTTPException(status_code=400, detail="missing_required_fields")
    
    user = user_model.password_update_user(user_id, data)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    return {"data": user}

# 회원탈퇴
def delete_user(user_id: int):
    user = user_model.delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")
    return {"data": user}