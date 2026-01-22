import random
from app.spatial.grid_utils import create_grid

def analyze_polygon_service(coordinates, area):
    grid_cells = create_grid(coordinates)

    predictions = []

    for cell in grid_cells:
        probability = random.uniform(0.3, 0.9)
        category = "high" if probability >= 0.7 else "medium" if probability >= 0.4 else "low"

        predictions.append({
            "cell_id": cell["id"],
            "center": cell["center"],
            "corners": cell["corners"],
            "probability": round(probability, 3),
            "category": category,
            "features": {
                "elevation": 0,
                "population": 0,
                "nightlights": 0,
                "built_up": 0,
                "ndvi": 0,
                "slope": 0
            }
        })

    return {
        "status": "success",
        "area": area,
        "grid_size": len(predictions),
        "gee_available": False,
        "predictions": predictions
    }
