# StreetSprint

Team Name: Group 158

Team Members: Edward Roshko, Matthew Shen, Trevor Turnquist

Project Title: StreetSprint

Problem: 
The problem is finding the fastest route between 2 points on a map.

Motivation: 
We use maps to find directions to a destination and we would prefer to have the shortest route.

Features: 
Map visualization
Plot fastest route between the two locations
Display distance between the two locations
Display time to find the path by the selected algorithm
We know we have solved the problem when the algorithm and visualization match the results we can obtain manually for small map sizes

Data: 
OpenStreetMap
The data is contained in XML format. There are multiple nodes with latitude and longitude values that represent points on the map. Nodes are grouped into ways, closed ways, areas, and relations, which represent roads, paths, areas, etc.
https://www.openstreetmap.org/export#map=13/52.3579/-2.0783

Tools:
Dash: Data Visualizer,
Folium: Map Display,
OSMnx: Parse Data

Strategy:
Dijkstra’s Algorithm,
Bellman-Ford Algorithm,
A* Algorithm

Distribution of Responsibility and Roles:
Edward: OSMnx,
Matthew: Dash,
Trevor: Folium

How To Run:
Type 'python3 page.py' in terminal then go to http://localhost:8050/. Select an algorithm and enter two locations / streets within
the black box on the map (make sure to type name exactly as shown on map).