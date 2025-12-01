from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def add_user(db: Session, user_data: dict):
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, data: dict):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def password_update_user(db: Session, user_id: int, data: dict):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.password = data["password"]
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user
