import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

class StreetSprint:
    def __init__(self):
        # Get graph for Gainesville
        self.G = ox.graph_from_place("Gainesville, Florida, USA", network_type="drive")

    def add_start_location(self, place_name):
        # Add a start location to the Street Sprint
        self.start_location = place_name

    def add_end_location(self, place_name):
        # Add an end location to the Street Sprint
        self.end_location = place_name

    def get_coordinates_from_location(self, place_name):
        # Get the coordinates of a location
        location =  ox.geocoder.geocode(place_name)

        # Check if location is found
        if location is None:
            return None
        else:
            return (location[0], location[1])

    def plot_map(self):
        # Plot the map with the start and end locations highlighted
        start_coords = self.get_coordinates_from_location(self.start_location)
        end_coords = self.get_coordinates_from_location(self.end_location)

        # Find the nearest nodes to the start and end locations
        start_node = ox.distance.nearest_nodes(self.G, start_coords[1], start_coords[0])
        end_node = ox.distance.nearest_nodes(self.G, end_coords[1], end_coords[0])

        # Find the shortest path between the start and end nodes
        shortest_path = nx.shortest_path(self.G, source=start_node, target=end_node, weight='length')

        # Plot the shortest path on the map
        fig, ax = ox.plot_graph_route(self.G, shortest_path, show=False, close=False)
        ax.scatter(start_coords[1], start_coords[0], c="red")
        ax.scatter(end_coords[1], end_coords[0], c="blue")

        # Show the map
        plt.show()

# Built-in function for finding shortest path
def networkx_shortest_path(graph, start, end):
    return nx.shortest_path(graph, source=start, target=end, weight="length")

# Dijkstra's Algorithm for finding shortest path
def dijkstra(graph, start, end):
    shortest_paths = {vertex: float('infinity') for vertex in graph}
    shortest_paths[start] = 0
    previous_nodes = {vertex: None for vertex in graph}
    nodes = set(graph.keys())

    while nodes:
        min_node = None
        for node in nodes:
            if min_node is None:
                min_node = node
            elif shortest_paths[node] < shortest_paths[min_node]:
                min_node = node
        
        if min_node == end:
            break

        nodes.remove(min_node)
        current_weight = shortest_paths[min_node]

        for edge in graph[min_node]:
            weight = current_weight + graph[min_node][edge]
            if weight < shortest_paths[edge]:
                shortest_paths[edge] = weight
                previous_nodes[edge] = min_node

    # Reconstruct the shortest path and calculate its length
    path, current_node = [], end
    while previous_nodes[current_node] is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    path.insert(0, start)

    return shortest_paths[end]