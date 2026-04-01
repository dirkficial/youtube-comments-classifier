from fastapi import APIRouter, HTTPException
from scraper import (parse_video_id, get_video_comments)
from classifier import classify_comments
from schemas import (AnalyzeRequest, AnalyzeResponse)


router = APIRouter(prefix="/api/analyze", tags=["analyze"])

# Creates analysis of a video
@router.post("/")
async def analyze_video(request: AnalyzeRequest):
    try: 
        video_id = parse_video_id(request.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Youtube URL")
    video_comments = get_video_comments(video_id)

    if not video_comments:
        raise HTTPException(status_code=404, detail="Comments not found!")
    
    results = classify_comments(video_comments)

    return AnalyzeResponse(
        video_id=video_id,
        total_comments=len(video_comments),
        actionable=sum(1 for r in results if r["category"] == "ACTIONABLE"),
        supportive=sum(1 for r in results if r["category"] == "SUPPORTIVE"),
        irrelevant=sum(1 for r in results if r["category"] == "IRRELEVANT"),
        comments=results
    )