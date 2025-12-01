from sqlalchemy import Column, Integer, String, Text, func
from sqlalchemy.orm import Session

from db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False, default="anonymous")


def get_posts(db: Session):
    return db.query(Post).all()


def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def get_post_by_title(db: Session, title: str):
    normalized = title.strip().lower()
    return (
        db.query(Post)
        .filter(func.lower(func.trim(Post.title)) == normalized)
        .first()
    )


def add_post(db: Session, post_data: dict):
    post = Post(**post_data)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post_id: int, data: dict):
    post = get_post_by_id(db, post_id)
    if not post:
        return None

    for key, value in data.items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int):
    post = get_post_by_id(db, post_id)
    if not post:
        return None

    db.delete(post)
    db.commit()
    return post
