import folium
from street_sprint import StreetSprint

s = StreetSprint()
bounds = s.get_map_bounds()

map = folium.Map(
  max_bounds = True,
  location = [29.6520, -82.3250],
  zoom_start = 12,
  min_lat = bounds[1],
  max_lat = bounds[3],
  min_lon = bounds[0],
  max_lon = bounds[2],
)

# Turns bounds array into array of points
boundsCoords = [
  [bounds[1], bounds[0]],
  [bounds[3], bounds[0]],
  [bounds[3], bounds[2]],
  [bounds[1], bounds[2]],
  [bounds[1], bounds[0]]
]

# Adds boundary to map
folium.PolyLine(
  locations = boundsCoords,
  color = "000000",
  weight = 5
).add_to(m)
