import app.models as models

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import get_db

router = APIRouter(prefix="/api/results", tags=["results"])

@router.get("/{video_id}")
def get_results(video_id: str, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.Analysis).where(models.Analysis.video_id == video_id)
    )

    analysis = result.scalars().first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video has not been previously analyzed"
        )

    return {
        "video_id" : video_id,
        "analyzed_at" : analysis.analyzed_at,
        "total_comments" : len(analysis.comments),
        "comments" : analysis.comments
    } 
