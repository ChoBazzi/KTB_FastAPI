# router/post_router.py
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from controller import post_controller

router = APIRouter(prefix="/post")


class PostCreate(BaseModel):
    title: str
    content: str
    author: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None


@router.get("")
def get_posts():
    return post_controller.get_posts()


@router.get("/{post_id}")
def get_post(post_id: int):
    return post_controller.get_post(post_id)


@router.post("", status_code=201)
def create_post(data: PostCreate):
    return post_controller.create_post(data.dict())


@router.put("/{post_id}")
def update_post(post_id: int, data: PostUpdate):
    return post_controller.update_post(post_id, data.dict())


@router.delete("/{post_id}")
def delete_post(post_id: int):
    return post_controller.delete_post(post_id)
