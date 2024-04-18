import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math
import queue
import time

class StreetSprint:
    def __init__(self):
        # Get graph for Gainesville
        self.G = ox.graph_from_place("Gainesville, Florida, USA", network_type="drive")

    def get_map_bounds(self):
        x_min = float('inf')
        y_min = float('inf')
        x_max = float('-inf')
        y_max = float('-inf')
        for node in self.G.nodes(data=True):
            if node[1]['x'] < x_min:
                x_min = node[1]['x']
            elif node[1]['x'] > x_max:
                x_max = node[1]['x']
            if node[1]['y'] < y_min:
                y_min = node[1]['y']
            elif node[1]['y'] > y_max:
                y_max = node[1]['y']

        return (x_min, y_min, x_max, y_max)


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
        start_time = time.time()
        if algorithm == "default":
            print('Finding shortest path using built-in function')
            dist, path = ShortestPath.networkx_shortest_path(self.G, start_node, end_node)
            end_time = time.time()
            print('Distance between nodes:', dist)
            print('Time taken:', end_time - start_time)
            print('\n')
        elif algorithm == "dijkstra":
            print('Finding shortest path using Dijkstra\'s algorithm')
            dist, path = ShortestPath.dijkstra(self.G, start_node, end_node)
            end_time = time.time()
            print('Distance between nodes:', dist)
            print('Time taken:', end_time - start_time)
            print('\n')
        elif algorithm == "bellman-ford":
            print('Finding shortest path using Bellman-Ford algorithm')
            dist, path = ShortestPath.bellman_ford(self.G, start_node, end_node)
            end_time = time.time()
            print('Distance between nodes:', dist)
            print('Time taken:', end_time - start_time)
            print('\n')
        elif algorithm == "floyd-warshall":
            dist = ShortestPath.floyd_warshall(self.G, start_node, end_node)
            print(dist)
            print(nx.shortest_path_length(self.G, source=start_node, target=end_node, weight="length"))
            return
        elif algorithm == "a-star":
            print('Finding shortest path using A* algorithm')
            dist, path = ShortestPath.a_star(self.G, start_node, end_node)
            end_time = time.time()
            print('Distance between nodes:', dist)
            print('Time taken:', end_time - start_time)
            print('\n')
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

        # Create a priority queue and add the start node
        pq = queue.PriorityQueue()
        pq.put((0, start))  # Priority queue stores tuples (distance, node)

        # Set to store visited nodes
        visited = set()

        while not pq.empty():
            # Get the node with the smallest known distance
            current_weight, min_node = pq.get()

            # Check if node has already been visited
            if min_node in visited:
                continue

            # Mark the node as visited
            visited.add(min_node)

            # Process each neighbor
            for neighbor in graph.successors(min_node):
                # Since it's a MultiDiGraph, iterate over all edges from min_node to neighbor
                for key, edge_data in graph[min_node][neighbor].items():
                    weight = edge_data.get('length', float('infinity')) + current_weight

                    # Only consider this new path if it's better
                    if weight < shortest_paths[neighbor]:
                        shortest_paths[neighbor] = weight
                        previous_nodes[neighbor] = min_node
                        pq.put((weight, neighbor))

        # Reconstruct the shortest path from end to start using previous_nodes
        path, current_node = [], end
        if previous_nodes[current_node] is not None or current_node == start:  # Ensure start=end case
            while current_node is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]

        return shortest_paths[end], path
    
    def bellman_ford(graph, start, end):
        # Initialize distance and predecessor dictionaries
        distances = {vertex: float('infinity') for vertex in graph}
        distances[start] = 0
        predecessors = {vertex: None for vertex in graph}

        # Relax all edges |V| - 1 times
        for _ in range(len(graph) - 1):
            # Relax edges from start node first, then order doesn't matter
            for u in graph:
                current_distance = distances[u]
                # Relax all neighbors of u
                for neighbor in graph.successors(u):
                    # Safely access the weight; default to some large number if no weight is given
                    weight = graph[u][neighbor][0].get('length', float('infinity'))
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        predecessors[neighbor] = u

        # Assume no negative cycles

        # Reconstruct the path
        path = []
        step = end
        if distances[end] == float('infinity'):
            return float('infinity'), []  # Unreachable

        while step is not None:
            path.insert(0, step)
            step = predecessors[step]

        return distances[end], path

    # Floyd-Warshall Algorithm for finding shortest path
    def floyd_warshall(graph, start, end):
        # Create a 2D dictionary to store the distances between nodes, initialized to infinity
        dist = {node: {v: float('infinity') for v in graph} for node in graph}
        # Initialize the diagonal to 0 (distance to self is 0)
        for node in graph:
            dist[node][node] = 0

        # Initialize a predecessor matrix
        next = {node: {v: None for v in graph} for node in graph}

        # Add the edge distances to the dist matrix
        for u, v, data in graph.edges(data=True):
            dist[u][v] = data.get('length', float('infinity'))
            next[u][v] = v

        # Floyd-Warshall algorithm
        for k in graph:
            for i in graph:
                for j in graph:
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next[i][j] = next[i][k]

        # Reconstruct the shortest path
        path = []
        while start != end:
            if next[start][end] is None:
                return float('infinity'), []
            path.append(start)
            start = next[start][end]
        path.append(end)

        return dist[start][end]
    
    def calculate_euclidean(graph, node1, node2):
        # Calculate the Euclidean distance between two nodes
        x1, y1 = graph.nodes[node1]['x'], graph.nodes[node1]['y']
        x2, y2 = graph.nodes[node2]['x'], graph.nodes[node2]['y']
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def a_star(graph, start, end):
        # Create a priority queue to store the nodes to be processed
        pq = queue.PriorityQueue()
        
        # Create a dictionary to store the shortest path distance to each node
        shortest_paths = {vertex: float('infinity') for vertex in graph.nodes()}
        shortest_paths[start] = 0
        
        # Create a dictionary to store heuristic scores for each node
        heuristic_scores = {vertex: ShortestPath.calculate_euclidean(graph, vertex, end) for vertex in graph.nodes()}
        
        # Create a dictionary to store the previous node in the shortest path
        previous_nodes = {vertex: None for vertex in graph.nodes()}
        
        # Add the start node to the priority queue
        pq.put((shortest_paths[start] + heuristic_scores[start], start))
        
        while not pq.empty():
            # Get the node with the lowest f_score from the priority queue
            current_distance, current_vertex = pq.get()
            
            # If the end node is reached, stop the search
            if current_vertex == end:
                break
            
            # Iterate through each neighbor of the current node
            for neighbor in graph.neighbors(current_vertex):
                # Iterate through each edge between current_vertex and neighbor
                for key, edge_data in graph[current_vertex][neighbor].items():
                    edge_weight = edge_data['length']
                    distance_through_vertex = shortest_paths[current_vertex] + edge_weight
                    
                    # If a shorter path to the neighbor is found, update the path
                    if distance_through_vertex < shortest_paths[neighbor]:
                        shortest_paths[neighbor] = distance_through_vertex
                        previous_nodes[neighbor] = current_vertex
                        # Recalculate f_score and add to the priority queue
                        f_score = distance_through_vertex + heuristic_scores[neighbor]
                        pq.put((f_score, neighbor))
        
        # Reconstruct the path from end to start using previous_nodes
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes[current]
        
        # Return the reversed path (from start to end)
        path.reverse()
        return shortest_paths[end], path
    
    def GetCoordinatesFromNode(graph, node):
        return (graph.nodes[node]['y'], graph.nodes[node]['x'])
    
    def GetCoordinatesFromPath(graph, path):
        return [ShortestPath.GetCoordinatesFromNode(graph, node) for node in path]