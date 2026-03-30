from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    url: str

class CommentResult(BaseModel):
    comment_text: str
    like_count: int
    reply_count: int
    category: str
    summary: str
    importance: str

class AnalyzeResponse(BaseModel):
    video_id: str
    total_comments: str | None = None
    positive: int | None = None
    negative: int | None = None
    garbage: int | None = None
    comments: list[CommentResult]
