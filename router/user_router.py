# routers/user_router.py
from fastapi import APIRouter
from controller import user_controller
from pydantic import BaseModel

router = APIRouter(prefix="/user")

class UserUpdate(BaseModel):
    name: str
    email: str

class passwordUpdate(BaseModel):
    password: str

# 전체 사용자 목록 조회
@router.get("")
def get_users():
    return user_controller.get_users()

# 특정 사용자 상세 조회
@router.get("/{user_id}")
def get_user(user_id: int):
    return user_controller.get_user(user_id)

# 사용자 생성 (201 Created)
@router.post("", status_code=201)
def create_user(data: dict):
    return user_controller.create_user(data)

# 로그인 
@router.post("/login")
def login(data: dict):
    return user_controller.login(data)

# 회원정보 수정
@router.put("/profile/{user_id}")
def update_user(user_id: int, data: UserUpdate):
    return user_controller.update_user(user_id, data.dict())

# 비밀번호 수정
@router.put("/password_up/{user_id}")
def password_update_user(user_id: int, data: passwordUpdate):
    return user_controller.password_update_user(user_id, data.dict())

# 회원탈회 
@router.delete("/{user_id}")
def delete_user(user_id: int):
    return user_controller.delete_user(user_id)
  