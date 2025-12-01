# controllers/user_controller.py
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from model import user_model

# 사용자 목록 조회
def get_users(db: Session):
    users = user_model.get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="no_users_found")
    return {"data": jsonable_encoder(users)}

# 특정 사용자 상세 조회
def get_user(db: Session, user_id: int):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_user_id")
    user = user_model.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")

    return {"data": jsonable_encoder(user)}

# 사용자 생성
# 패스워드 추가 - 암호화작업x
def create_user(db: Session, data: dict):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="missing_required_fields")

    if user_model.get_user_by_email(db, email):
        raise HTTPException(status_code=409, detail="email_already_exists")

    new_user = {"name": name, "email": email, "password": password}
    user = user_model.add_user(db, new_user)
    return {"data": jsonable_encoder(user)}

# 로그인
def login(db: Session, data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="missing_email or password")

    user = user_model.get_user_by_email(db, email)
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="unauthorized")

    return {"data": {"user_id": user.id, "name": user.name}}

# 회원정보 수정
def update_user(db: Session, user_id: int, data: dict):

    email = data.get("email")
    name = data.get("name")

    if not name:
        raise HTTPException(status_code=400, detail="missing_required_fields")
    
    user = user_model.update_user(db, user_id, data)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    return {"data": jsonable_encoder(user)}

# 비밀번호 변경
def password_update_user(db: Session, user_id: int, data: dict):

    password = data.get("password")

    if not password:
        raise HTTPException(status_code=400, detail="missing_required_fields")
    
    user = user_model.password_update_user(db, user_id, data)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    return {"data": jsonable_encoder(user)}

# 회원탈퇴
def delete_user(db: Session, user_id: int):
    user = user_model.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")
    return {"data": jsonable_encoder(user)}
