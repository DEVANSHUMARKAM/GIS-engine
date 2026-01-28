from fastapi import APIRouter # type: ignore
from app.schemas.request import AnalyzeRequest
from app.services.analysis_service import analyze_polygon_service

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "GIS Development Predictor"
    }

@router.post("/analyze")
def analyze_polygon(payload: AnalyzeRequest):
    return analyze_polygon_service(
        coordinates=payload.coordinates,
        area=payload.area
    )
