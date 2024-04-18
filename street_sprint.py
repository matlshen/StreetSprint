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

    def get_shortest_path(self, algorithm):
        # Find the shortest path between the start and end locations
        start_coords = self.get_coordinates_from_location(self.start_location)
        end_coords = self.get_coordinates_from_location(self.end_location)

        # Find the nearest nodes to the start and end locations
        start_node = ox.distance.nearest_nodes(self.G, start_coords[1], start_coords[0])
        end_node = ox.distance.nearest_nodes(self.G, end_coords[1], end_coords[0])

        # Get the length of the shortest path
        if algorithm == "default":
            dist, path = ShortestPath.networkx_shortest_path(self.G, start_node, end_node)
        elif algorithm == "dijkstra":
            dist, path = ShortestPath.dijkstra(self.G, start_node, end_node)
        elif algorithm == "floyd-warshall":
            dist, path = ShortestPath.floyd_warshall(self.G, start_node, end_node)
        else:
            raise ValueError("Invalid algorithm")

        # Plot the shortest path on the map
        fig, ax = ox.plot_graph_route(self.G, path, show=False, close=False)
        ax.scatter(start_coords[1], start_coords[0], c="red")
        ax.scatter(end_coords[1], end_coords[0], c="blue")

        plt.show()

class ShortestPath:
    # Built-in function for finding shortest path
    def networkx_shortest_path(graph, start, end):
        path =  nx.shortest_path(graph, source=start, target=end, weight="length")
        dist = nx.shortest_path_length(graph, source=start, target=end, weight="length")
        return dist, path

    # Dijkstra's Algorithm for finding shortest path
    def dijkstra(graph, start, end):
        # Create dictionary to store shortest distance to each node
        shortest_paths = {vertex: float('infinity') for vertex in graph.nodes()}
        shortest_paths[start] = 0

        # Create dictionary to store the previous node in the shortest path
        previous_nodes = {vertex: None for vertex in graph.nodes()}

        # Create a set to store the nodes that have not been visited
        nodes = set(graph.nodes())

        # Loop until all nodes have been visited
        while nodes:
            # Find node with the smallest known distance
            # TODO: Possible optimization storing shortest path
            min_node = None
            for node in nodes:
                if min_node is None or shortest_paths[node] < shortest_paths[min_node]:
                    min_node = node
            
            # Break if the smallest distance node is unreachable
            if min_node is None or shortest_paths[min_node] == float('infinity'):
                break
            
            nodes.remove(min_node)
            current_weight = shortest_paths[min_node]

            # Process each neighbor
            for neighbor in graph.successors(min_node):
                # Safely access the weight; default to some large number if no weight is given
                weight = graph[min_node][neighbor][0].get('length', float('infinity')) + current_weight
                if weight < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = weight
                    previous_nodes[neighbor] = min_node

        # Reconstruct the shortest path and calculate its length
        path, current_node = [], end
        if previous_nodes[current_node] is not None or current_node == start:  # Ensure start=end case
            while current_node is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]

        return shortest_paths[end], path

    # Floyd-Warshall Algorithm for finding shortest path
    def floyd_warshall(graph, start, end):
        # Create a 2D dictionary to store the distances between nodes, initialized to infinity
        dist = {node: {v: float('infinity') for v in graph} for node in graph}

        # Initialize a predecessor matrix
        next = {node: {v: None for v in graph} for node in graph}