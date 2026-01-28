from pydantic import BaseModel # type: ignore
from typing import List, Dict

class CellPrediction(BaseModel):
    cell_id: int
    center: List[float]
    corners: List[List[float]]
    probability: float
    category: str
    features: Dict[str, float]

class AnalyzeResponse(BaseModel):
    status: str
    area: float
    grid_size: int
    gee_available: bool
    predictions: List[CellPrediction]
