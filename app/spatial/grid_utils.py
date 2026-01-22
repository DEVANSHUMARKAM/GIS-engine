from shapely.geometry import Polygon, box
import math

def create_grid(coordinates, cell_size_meters=500):
    polygon = Polygon([(c[1], c[0]) for c in coordinates])
    minx, miny, maxx, maxy = polygon.bounds

    lat_center = (miny + maxy) / 2
    meters_per_degree_lat = 111320
    meters_per_degree_lng = 111320 * math.cos(math.radians(lat_center))

    cell_lat = cell_size_meters / meters_per_degree_lat
    cell_lng = cell_size_meters / meters_per_degree_lng

    grid = []
    cell_id = 0
    y = miny

    while y < maxy:
        x = minx
        while x < maxx:
            cell_box = box(
                x, y,
                min(x + cell_lng, maxx),
                min(y + cell_lat, maxy)
            )

            if cell_box.intersects(polygon):
                intersection = cell_box.intersection(polygon)
                center = intersection.centroid
                bounds = cell_box.bounds

                grid.append({
                    "id": cell_id,
                    "center": [center.y, center.x],
                    "corners": [
                        [bounds[1], bounds[0]],
                        [bounds[3], bounds[0]],
                        [bounds[3], bounds[2]],
                        [bounds[1], bounds[2]],
                        [bounds[1], bounds[0]]
                    ]
                })
                cell_id += 1
            x += cell_lng
        y += cell_lat

    return grid
