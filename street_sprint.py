import networkx as nx
import osmnx as ox
import matplotlib
matplotlib.use('TkAgg') # no UI backend

import matplotlib.pyplot as plt
import numpy as np

ox_graph = ox.graph_from_place("Gainesville, Florida, USA", network_type="drive")
fig, ax = ox.plot_graph(ox_graph)
plt.show()