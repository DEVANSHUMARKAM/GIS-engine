import math
import random
from app.spatial.grid_utils import create_grid

def get_dist_point_to_line(point, line_start, line_end):
    """
    Calculates the shortest perpendicular distance from a point [lat, lng] 
    to a line segment (the road).
    
    Math Concept: Linear Algebra (Distance from point to line)
    """
    y, x = point       # The grid cell center
    y1, x1 = line_start # Start of the road
    y2, x2 = line_end   # End of the road

    # A, B, C derive from the standard line equation Ax + By + C = 0
    A = y1 - y2
    B = x2 - x1
    C = (x1 * y2) - (x2 * y1)

    # Denominator handles the length of the line segment
    denom = math.sqrt(A**2 + B**2)
    
    # Avoid division by zero if the line is a single point
    if denom == 0:
        return 0.0

    # Perpendicular distance formula: |Ax + By + C| / sqrt(A^2 + B^2)
    distance = abs(A * x + B * y + C) / denom
    return distance

def analyze_polygon_service(coordinates, area):
    """
    Core logic for Urban Growth Prediction.
    Instead of random guessing, we now use a 'Weighted Suitability Model'.
    Drivers:
    1. Distance to City Center (Gravity Model)
    2. Distance to Major Roads (Ribbon Development Model)
    """
    
    # 1. Generate the grid from the polygon geometry
    grid_cells = create_grid(coordinates)
    predictions = []

    # --- PHASE 1: SETUP GROWTH DRIVERS ---
    
    # Driver A: City Center (Calculated as the geometric center of polygon)
    avg_lat = sum(c[0] for c in coordinates) / len(coordinates)
    avg_lng = sum(c[1] for c in coordinates) / len(coordinates)
    city_center = [avg_lat, avg_lng]

    # Driver B: The Highway (Simulated)
    # Creating a virtual road from Bottom-Left to Top-Right of the area
    bounds_min_lat = min(c[0] for c in coordinates)
    bounds_min_lng = min(c[1] for c in coordinates)
    bounds_max_lat = max(c[0] for c in coordinates)
    bounds_max_lng = max(c[1] for c in coordinates)
    
    road_start = [bounds_min_lat, bounds_min_lng]
    road_end = [bounds_max_lat, bounds_max_lng]

    # Scaling Factors
    # "Max Influence" = How far away does the effect stop mattering?
    # 0.03 degrees is roughly 3km. Beyond this, probability drops to 0.
    max_influence_dist = 0.03 

    # --- PHASE 2: ANALYZE EACH CELL ---
    for cell in grid_cells:
        
        # 1. Calculate Raw Distances (Physics)
        dist_center = math.sqrt((cell["center"][0] - city_center[0])**2 + 
                                (cell["center"][1] - city_center[1])**2)
        
        dist_road = get_dist_point_to_line(cell["center"], road_start, road_end)

        # 2. Normalize Scores (0.0 to 1.0)
        # 1.0 means "Very close" (High growth potential)
        # 0.0 means "Far away" (Low growth potential)
        score_center = max(0, 1 - (dist_center / max_influence_dist))
        score_road = max(0, 1 - (dist_road / max_influence_dist))

        # 3. Apply Weights (The "Algorithm")
        # Roads are slightly more important (60%) than the old center (40%)
        base_probability = (score_center * 0.4) + (score_road * 0.6)

        # 4. Add "Organic" Noise
        # Real cities aren't perfect math equations. We add ±5% randomness.
        noise = random.uniform(-0.05, 0.05)
        final_probability = base_probability + noise
        
        # Clamp result to ensure it stays between 0% and 100%
        final_probability = max(0.0, min(1.0, final_probability))

        # 5. Categorize
        category = "high" if final_probability >= 0.7 else "medium" if final_probability >= 0.4 else "low"

        predictions.append({
            "cell_id": cell["id"],
            "center": cell["center"],
            "corners": cell["corners"],
            "probability": round(final_probability, 3),
            "category": category,
            "features": {
                "dist_center": round(dist_center, 4),
                "dist_road": round(dist_road, 4),
                "score_center": round(score_center, 2),
                "score_road": round(score_road, 2)
            }
        })

    return {
        "status": "success",
        "area": area,
        "grid_size": len(predictions),
        "gee_available": False,
        "predictions": predictions
    }