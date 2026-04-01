from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from sqlalchemy import select, models
from schemas import (UserResponse, UserCreate)
from db import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/",
             response_model=UserResponse,
             status_code=201
             )
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.username == user.username)
        )
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    
    result = db.execute(
        select(models.User).where(models.User.email == user.email)
        )
    existing_email = result.scalars().first()
    
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    