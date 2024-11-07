import matplotlib.pyplot as plt
import networkx as nx
from rdflib import Graph, Namespace, RDFS

# Load the RDF data
g = Graph()
g.parse("odissei.ttl", format="ttl")

# Define namespaces
odissei = Namespace("https://w3id.org/odissei/ns/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Extract classes and relationships
classes = set()
relationships = []
for s, p, o in g:
    if str(s).startswith(str(odissei)):
        classes.add(s)
    if p == rdfs.subClassOf or p == rdfs.domain or p == rdfs.range:
        relationships.append((s, p, o))

# Create a directed graph
G = nx.DiGraph()

# Add nodes (classes)
G.add_nodes_from(classes)

# Add edges (relationships) with labels
for s, p, o in relationships:
    label = p.split("#")[-1]  # Extract label from predicate
    G.add_edge(s, o, label=label)

# Plot the graph
plt.figure(figsize=(12, 8), dpi=300)  # Increase figure size and DPI for higher resolution
pos = nx.spring_layout(G, seed=42)  # Seed for consistent layout

node_sizes = [len(node.split("#")[-1]) * 100 for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue', node_shape='s')
nx.draw_networkx_edges(G, pos, arrowsize=20, width=2, edge_color='gray')
nx.draw_networkx_labels(G, pos, labels={node: node.split("#")[-1] for node in G.nodes()}, font_size=14, font_weight='bold', font_color='black')
nx.draw_networkx_edge_labels(G, pos, edge_labels=dict(G.edges), font_size=12)
plt.axis('off')

# Save the graph as a high-quality PNG image
plt.savefig('odissei_graph_from_rdflib.png', dpi=300, bbox_inches='tight')

plt.show()
