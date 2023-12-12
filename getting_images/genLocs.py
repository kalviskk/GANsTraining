import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
import atexit
import osmnx as ox
# Assuming 'polygons.txt' is a CSV file with 'lat' and 'lon' columns
dati = pd.read_csv("polygons.txt")
# Define the list of cities you're interested in
cities = ["London", "Paris", "Madrid", "Milan", "Manchester", "Frankfurt"]  # Add more cities as needed




def create_polygons_from_dataframe(dataframe):
    polygons = []
    current_polygon_coords = []

    for _, row in dataframe.iterrows():
        # Check for NaN values which indicate separation between polygons
        if pd.isna(row['lat']) or pd.isna(row['lon']):
            if current_polygon_coords:
                polygons.append(Polygon(current_polygon_coords))
                current_polygon_coords = []
        else:
            current_polygon_coords.append((row['lon'], row['lat']))

    # Add the last polygon if the DataFrame doesn't end with NaN
    if current_polygon_coords:
        polygons.append(Polygon(current_polygon_coords))

    return polygons

polygons = create_polygons_from_dataframe(dati)

def load_previous_locations(filename):
    try:
        return np.load(filename, allow_pickle=True)
    except FileNotFoundError:
        return np.empty((0, 2), dtype=float)

def save_previous_locations(filename, locations):
    np.save(filename, locations, allow_pickle=True)

def generate_grid_inside_polygon(polygon, spacing_km):
    # Convert spacing from kilometers to approximate degrees
    spacing_deg = spacing_km / 111  # Roughly 111km per degree
    minx, miny, maxx, maxy = polygon.bounds
    x_coords = np.arange(minx, maxx, spacing_deg)
    y_coords = np.arange(miny, maxy, spacing_deg)
    
    grid_points = []
    for x in x_coords:
        for y in y_coords:
            point = Point(x, y)
            if polygon.contains(point):
                grid_points.append((y, x))  # Save as (lat, lon)
    
    return np.array(grid_points)

def exit_handler():
    print(f"Saving {len(previous_locations)} locations before exiting.")
    save_previous_locations(prev_locs_filename, previous_locations)

# Register the handler
atexit.register(exit_handler)

# Read the polygon data from a CSV file
# dati = pd.read_csv("polygons.txt")



for city in cities:
    # This will give you the boundary of the city
    city_boundary = ox.geocode_to_gdf(city)
    print(f"{city} Boundary: \n{city_boundary.geometry}")
    
polygons = create_polygons_from_dataframe(dati)

prev_locs_filename = 'prevLocs2.npy'
previous_locations = load_previous_locations(prev_locs_filename)

# Specify the spacing for the grid in kilometers
grid_spacing_km = 1.0

# Generate the grid points for each polygon
for polygon in polygons:
    grid_points = generate_grid_inside_polygon(polygon, grid_spacing_km)
    previous_locations = np.vstack((previous_locations, grid_points)) if previous_locations.size else grid_points

# Save the generated grid points
save_previous_locations(prev_locs_filename, previous_locations)

print(f"Generated a grid of {len(previous_locations)} locations inside the polygon.")

