# from scraper import get_video_comments, parse_video_id
# from classifier import classify_comments, save_response

# url = input("Enter YouTube video URL: ")
# video_id = parse_video_id(url)

# print(f"Fetching comments for video: {video_id}")
# comments = get_video_comments(video_id)

# print(f"Found {len(comments)} comments. Classifying...")
# results = classify_comments(comments)

# save_response(results)
# print("Done! Results saved to output/results.csv")
from enum import Enum
from fastapi import FastAPI
from app.routes.analyze import router as analyze_router

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

# Starts Here

@app.get("/health")
def health_check():
    return {"status" : "ok"}

# Create an analysis of a video
app.include_router(analyze_router)

# Get previous results of a certain video
@app.get("/api/results/{video_id}")
async def get_analysis(video_id: str):
    return

@app.get