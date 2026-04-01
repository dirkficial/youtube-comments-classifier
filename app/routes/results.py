from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/results", tags=["results"])

@router.get("/")
def get_results():
    return