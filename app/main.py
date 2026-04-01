from fastapi import FastAPI
from routes.analyze import router as analyze_router

app = FastAPI(
    title="YouTube Comment Classifier",
    description="Analyzes YouTube comments and classifies them as actionable, supportive, or irrelevant"
)

# Starts Here

@app.get("/health")
def health_check():
    return {"status" : "ok"}

# Create an analysis of a video
app.include_router(analyze_router)

# Get previous results of a certain video
# @app.get("/api/results/{video_id}")
# async def get_analysis(video_id: str):
#     return
