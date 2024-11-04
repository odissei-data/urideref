import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges with labels
G.add_nodes_from(['ODISSEI', 'Variable\nthesaurus', 'Projects', 'Papers', 'Code\nlibrary'])
G.add_edges_from([
    ('ODISSEI', 'Variable\nthesaurus', {'label': 'Describe attributes\nfrom ODISSEI'}),
    ('ODISSEI', 'Projects', {'label': 'Provides data\n(CBS metadata)'}),
    ('Projects', 'Papers', {'label': 'Produces'}),
    ('Projects', 'Code\nlibrary', {'label': 'Produces\nsource-code for'})
])

# Plot the graph
plt.figure(figsize=(12, 8), dpi=300)  # Increase figure size and DPI for higher resolution
pos = nx.spring_layout(G, seed=42)  # Seed for consistent layout

# Create node labels with larger font size and adjust node size accordingly
node_labels = {node: f"\n{node}" for node in G.nodes()}
node_sizes = [len(label) * 100 for label in node_labels.values()]

nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue', node_shape='o')
nx.draw_networkx_edges(G, pos, arrowsize=20, width=2, edge_color='gray')
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=14, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'), font_size=12)
plt.axis('off')

# Save the graph as a high-quality PNG image
plt.savefig('odissei_graph_high_quality_with_node_text.png', dpi=300, bbox_inches='tight')

plt.show()