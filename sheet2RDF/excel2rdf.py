import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, SKOS
import os

# Load your Excel file
excel_file = 'file.xlsx'

# Read Excel sheet into a pandas DataFrame
df = pd.read_excel(excel_file)

# Initialize an RDF graph
g = Graph()

# Define namespaces
DATA_METHODS = Namespace("https://w3id.org/datamethods#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

# Bind namespaces to prefixes
g.bind("dm", DATA_METHODS)
g.bind("skos", SKOS)

# Iterate over rows in the DataFrame and create RDF triples
for index, row in df.iterrows():
    # Assuming you have columns "ID", "Label", and "Description" in your Excel sheet
    
    subject_uri = URIRef(DATA_METHODS[str(row['ID'])])  # Create a unique URI for each row
    label = Literal(row['Label'])  # The label (name) of the entity
    description = Literal(row['Description'])  # The description of the entity

    # Add RDF triples to the graph
    g.add((subject_uri, RDF.type, SKOS.Concept))
    g.add((subject_uri, SKOS.prefLabel, label))
    g.add((subject_uri, SKOS.definition, description))

# Load external ontology (DataMethods)
ontology_url = "https://raw.githubusercontent.com/ritamargherita/DataMethods/main/DataMethods.ttl"
g.parse(ontology_url, format="ttl")

# Serialize the RDF graph into Turtle format and save to a file
output_file = 'output_rdf.ttl'
g.serialize(destination=output_file, format='turtle')

print(f"RDF data successfully saved to {output_file}")
