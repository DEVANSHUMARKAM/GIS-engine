from pydantic import BaseModel # type: ignore
from typing import List

class AnalyzeRequest(BaseModel):
    coordinates: List[List[float]]  # [[lat, lng], ...]
    area: float
