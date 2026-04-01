from fastapi import APIRouter, HTTPException
from models import Analysis

router = APIRouter(prefix="/api/results", tags=["results"])

@router.get("/")
def get_results():
    