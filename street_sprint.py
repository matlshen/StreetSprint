import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

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




# Get a graph for a specific place
G = ox.graph_from_place("Gainesville, Florida, USA", network_type="drive")

# Get some attributes about the graph
print("node count:", len(G.nodes()))
print("edge count:", len(G.edges()))

# Locations
# The Hub (29.64826, -82.34601)
# Beque Holic (29.65262, -82.38104)

# Find nearest nodes to the given coordinates
bh_node_id = ox.distance.nearest_nodes(G, -82.38094, 29.65293)
hub_node_id = ox.distance.nearest_nodes(G, -82.34601, 29.64826)

print("Beque Holic node id:", bh_node_id)
print("The Hub node id:", hub_node_id)

# Print node data
print(G.nodes.get(bh_node_id)["x"], G.nodes.get(bh_node_id)["y"])
print(G.nodes.get(hub_node_id)["x"], G.nodes.get(hub_node_id)["y"])

# Find shortest path and its length
shortest_path = nx.shortest_path(G, source=bh_node_id, target=hub_node_id, weight='length')
shortest_distance = nx.shortest_path_length(G, source=bh_node_id, target=hub_node_id, weight='length')
print("Shortest distance:", shortest_distance)

# Plot shortest path on the map
fig, ax = ox.plot_graph_route(G, shortest_path, show=False, close=False)
ax.scatter(G.nodes.get(bh_node_id)["x"], G.nodes.get(bh_node_id)["y"], c="red")
ax.scatter(G.nodes.get(hub_node_id)["x"], G.nodes.get(hub_node_id)["y"], c="blue")
plt.show()


# Get shortest path using Dijkstra's Algorithm
shortest_path = dijkstra(G, bh_node_id, hub_node_id)
print(shortest_path)