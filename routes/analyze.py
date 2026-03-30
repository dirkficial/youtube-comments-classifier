from fastapi import APIRouter
from app.scraper import (parse_video_id, get_video_comments)
from app.classifier import classify_comments


router = APIRouter(prefix="/api/analyze", tags=["analze"])

# 
@router.post("/api/analyze")
async def analyze_url(url: str):
    video_id = parse_video_id(url)
    video_comments = get_video_comments(video_id)
    results = classify_comments(video_comments)

    return {"results" : results}