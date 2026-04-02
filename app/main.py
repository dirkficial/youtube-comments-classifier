from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes.analyze import router as analyze_router
from app.routes.results import router as results_router

from app.db import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="YouTube Comment Classifier",
    description="Analyzes YouTube comments and classifies them as actionable, supportive, or irrelevant",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {"status" : "ok"}

app.include_router(analyze_router)
app.include_router(results_router)