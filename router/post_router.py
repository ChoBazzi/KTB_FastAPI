# router/post_router.py
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from controller import post_controller
from db import get_db

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
def get_posts(db: Session = Depends(get_db)):
    return post_controller.get_posts(db)


@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    return post_controller.get_post(db, post_id)


@router.post("", status_code=201)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    return post_controller.create_post(db, data.dict())


@router.put("/{post_id}")
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):
    return post_controller.update_post(db, post_id, data.dict())


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return post_controller.delete_post(db, post_id)
