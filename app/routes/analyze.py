from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.db import get_db
from app.scraper import parse_video_id, get_video_comments
from app.classifier import classify_comments
from app.models import Analysis, Comment
from app.schemas import AnalyzeRequest, AnalyzeResponse

router = APIRouter(prefix="/api/analyze", tags=["analyze"])

# Creates analysis of a video
@router.post("/")
def analyze_video(request: AnalyzeRequest, db: Annotated[Session, Depends(get_db)]):

    video_id = parse_video_id(request.url)

    if not video_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Youtube URL")
        
    video_comments = get_video_comments(video_id)

    if not video_comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comments not found!")
    
    results = classify_comments(video_comments)

    analysis = Analysis(video_id = video_id)
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    for r in results:
        comment = Comment(
            analysis_id=analysis.id,
            comment_text=r["comment_text"],
            like_count=r["like_count"],
            reply_count=r["reply_count"],
            category=r["category"],
            summary=r["summary"],
            importance=r["importance"]
        )
        db.add(comment)
    db.commit()

    return AnalyzeResponse(
        video_id=video_id,
        total_comments=len(video_comments),
        actionable=sum(1 for r in results if r["category"] == "ACTIONABLE"),
        supportive=sum(1 for r in results if r["category"] == "SUPPORTIVE"),
        irrelevant=sum(1 for r in results if r["category"] == "IRRELEVANT"),
        comments=results
    )