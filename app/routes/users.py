from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
import app.models as models
from app.schemas import (UserResponse, UserCreate)
from app.db import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/",
             response_model=UserResponse,
             status_code=status.HTTP_201_CREATED
             )
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.email == user.email)
        )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    new_user = models.User(
        email=user.email,
        hashed_password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
