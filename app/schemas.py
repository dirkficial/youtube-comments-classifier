from pydantic import BaseModel
from datetime import datetime

class AnalyzeRequest(BaseModel):
    url: str

class CommentResult(BaseModel):
    comment_text: str
    like_count: int
    reply_count: int
    category: str
    summary: str
    importance: str

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

class UserCreate(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AnalyzeResponse(BaseModel):
    video_id: str
    total_comments: int
    actionable: int
    supportive: int
    irrelevant: int
    comments: list[CommentResult]

class AnalysisSummary(BaseModel):
    id: int
    video_id: str
    video_title: str | None
    total_comments: int
    analyzed_at: datetime