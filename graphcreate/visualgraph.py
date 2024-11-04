import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
G.add_nodes_from(['ODISSEI', 'Variable_thesaurus', 'Projects', 'Papers', 'Code_library'])
G.add_edges_from([('ODISSEI', 'Variable_thesaurus'), ('ODISSEI', 'Projects'), ('Projects', 'Papers'), ('Projects', 'Code_library')])

# Plot the graph
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)  # Position nodes using spring layout
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
nx.draw_networkx_edges(G, pos, arrowsize=20, width=2)
nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
plt.axis('off')
plt.show()
