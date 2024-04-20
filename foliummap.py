import folium
from street_sprint import StreetSprint
from shapely.geometry import Point, Polygon

s = StreetSprint()
bounds = s.get_map_bounds()

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

    folium.PolyLine(
      locations = boundsCoords,
      color = "#000000",
      weight = 5
    ).add_to(self.m)

    shortestPath = folium.PolyLine(
      locations=coords,
      color = "#FF0000",
      weight = 5
    )
    shortestPath.add_to(self.m)
    

  def updatePath(self, coords):
    #shortestPath.locations = coords
    shortestPath = folium.PolyLine(
      locations=coords,
      color = "#FF0000",
      weight = 5
    )
    shortestPath.add_to(self.m)

  def getMap(self):
    return self.m



# 0: min_lon, 1: min_lat, 2: max_lon, 3: max_lat
# Turns bounds array into array of points

points = []

"""
def handle_click(e):
    lat, lon = e.latlng
    print("Latitude:", lat)
    print("Longitude:", lon)

# Create a ClickForMarker plugin to allow users to add markers by clicking on the map
click_for_marker = folium.ClickForMarker().add_to(m)

# Adds boundary to map
"""


