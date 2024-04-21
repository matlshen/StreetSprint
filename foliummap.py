import folium
from street_sprint import StreetSprint

s = StreetSprint()
bounds = s.get_map_bounds()

# Coordinates for the boundary of Gainseville
boundsCoords = [
  [bounds[1], bounds[0]],
  [bounds[3], bounds[0]],
  [bounds[3], bounds[2]],
  [bounds[1], bounds[2]],
  [bounds[1], bounds[0]],
]

class Map:
  def __init__(self):
    self.createMap([[0,0]])

  # Creates a new map with the coordinates for the shortest path
  def createMap(self, coords):
    self.m = folium.Map(
      max_bounds = True,
      location = [29.6520, -82.3250],
      zoom_start = 12,
      min_lat = bounds[1],
      max_lat = bounds[3],
      min_lon = bounds[0],
      max_lon = bounds[2],
    )

    # PolyLine of the Gainesville boundary
    folium.PolyLine(
      locations = boundsCoords,
      color = "#000000",
      weight = 5
    ).add_to(self.m)

    # Shortest path PolyLine
    shortestPath = folium.PolyLine(
      locations=coords,
      color = "#FF0000",
      weight = 5
    )
    shortestPath.add_to(self.m)

  # Returns the map
  def getMap(self):
    return self.m


