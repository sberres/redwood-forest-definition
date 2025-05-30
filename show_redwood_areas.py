import geopandas as gpd
import folium
from shapely.geometry import Polygon
import pandas as pd

# Define approximate coordinates for Redwood areas (longitude and latitude)
# Note: These are example coordinates. Real GIS data should be used for precision.
redwood_areas = [
    {
        "name": "Redwood National and State Parks",
        "coords": [
            (-124.1, 41.7), (-123.9, 41.7), (-123.9, 41.3), (-124.1, 41.3)
        ]
    },
    {
        "name": "Prairie Creek Redwoods State Park",
        "coords": [
            (-124.05, 41.45), (-123.95, 41.45), (-123.95, 41.35), (-124.05, 41.35)
        ]
    },
    {
        "name": "Jedediah Smith Redwoods State Park",
        "coords": [
            (-124.15, 41.85), (-124.05, 41.85), (-124.05, 41.75), (-124.15, 41.75)
        ]
    },
    {
        "name": "Del Norte Coast Redwoods State Park",
        "coords": [
            (-124.15, 41.65), (-124.05, 41.65), (-124.05, 41.55), (-124.15, 41.55)
        ]
    },
    {
        "name": "Big Basin Redwoods State Park",
        "coords": [
            (-122.25, 37.25), (-122.15, 37.25), (-122.15, 37.15), (-122.25, 37.15)
        ]
    }
]

# Create a list of polygons and metadata
polygons = []
names = []
for area in redwood_areas:
    # Reverse coordinates for shapely (longitude, latitude)
    polygon = Polygon(area["coords"])
    polygons.append(polygon)
    names.append(area["name"])

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(
    {"name": names, "geometry": polygons},
    crs="EPSG:4326"  # WGS84 coordinate system
)

# Calculate map center (approximate center of California)
#map_center = [41.5, -123.5]
map_center = [41.6, -124.0]

# Create a Folium map without default tiles
m = folium.Map(
    location=map_center, 
    zoom_start=7,
    tiles=None  # No default tiles
)

# Add OpenStreetMap as alternative map layer
folium.TileLayer(
    tiles='OpenStreetMap',
    name='OpenStreetMap',
    overlay=False,
    control=True
).add_to(m)

# Add satellite imagery as the first (default) layer
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri World Imagery',
    name='Satellite Imagery',
    overlay=False,
    control=True
).add_to(m)



# Add polygons to the map
for idx, row in gdf.iterrows():
    # GeoJSON data from GeoDataFrame
    geo_j = gpd.GeoSeries(row.geometry).to_json()
    folium.GeoJson(
        geo_j,
        name=row["name"],
        style_function=lambda x: {
            "fillColor": "green",
            # "color": "darkgreen",
            "color": "blue",
            "weight": 2,
            "fillOpacity": 0.1
        },
        tooltip=row["name"]
    ).add_to(m)

# Add a legend (manually as HTML element)
legend_html = """
<div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; padding: 10px; background-color: white; border: 2px solid grey; border-radius: 5px;">
    <h4>Legend</h4>
    <p><span style="color: green;">████</span> Redwood Areas</p>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Add a layer control button
folium.LayerControl(collapsed=False).add_to(m)

# Save the map as HTML file
m.save("show_redwood_areas.html")

print("Map has been saved as 'show_redwood_areas.html'. Open the file in a browser to view the map.")
print("Karte wurde als 'show_redwood_areas.html' gespeichert. Öffnen Sie die Datei in einem Browser, um die Karte anzuzeigen.")