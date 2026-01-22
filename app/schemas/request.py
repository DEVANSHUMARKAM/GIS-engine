from pydantic import BaseModel
from typing import List

class AnalyzeRequest(BaseModel):
    coordinates: List[List[float]]  # [[lat, lng], ...]
    area: float
