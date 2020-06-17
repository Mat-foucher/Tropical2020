import networkx as nx 
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from([1,2])
G.add_edge(1,2)

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()