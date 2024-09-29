from flask import Flask, render_template_string, redirect, url_for
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD

app = Flask(__name__)

# Define namespaces
EX = Namespace("http://example.com/")
W3ID = Namespace("https://w3id.org/example/person/")

# Create an RDF graph (triple store)
g = Graph()

# Function to add example data to the triple store
def add_example_data():
    # Add Person 1 - John Doe
    person1 = URIRef(W3ID["1"])
    g.add((person1, RDF.type, FOAF.Person))
    g.add((person1, FOAF.name, Literal("John Doe", datatype=XSD.string)))
    g.add((person1, EX.age, Literal(30, datatype=XSD.integer)))
    g.add((person1, EX.occupation, Literal("Engineer", datatype=XSD.string)))

    # Add Person 2 - Jane Smith
    person2 = URIRef(W3ID["2"])
    g.add((person2, RDF.type, FOAF.Person))
    g.add((person2, FOAF.name, Literal("Jane Smith", datatype=XSD.string)))
    g.add((person2, EX.age, Literal(25, datatype=XSD.integer)))
    g.add((person2, EX.occupation, Literal("Doctor", datatype=XSD.string)))

    # Add Person 3 - Alice Johnson
    person3 = URIRef(W3ID["3"])
    g.add((person3, RDF.type, FOAF.Person))
    g.add((person3, FOAF.name, Literal("Alice Johnson", datatype=XSD.string)))
    g.add((person3, EX.age, Literal(40, datatype=XSD.integer)))
    g.add((person3, EX.occupation, Literal("Scientist", datatype=XSD.string)))

# Add example data to the graph when the script starts
add_example_data()

# HTML template for displaying RDF data (similar to DBpedia)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ person_name }} - RDF Data</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        table { width: 100%; border-collapse: collapse; }
        table, th, td { border: 1px solid #ddd; }
        th, td { padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>RDF Data for {{ person_name }}</h1>
    <table>
        <tr>
            <th>Property</th>
            <th>Value</th>
        </tr>
        {% for prop, value in rdf_data %}
        <tr>
            <td>{{ prop }}</td>
            <td>{{ value }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Route for redirecting from person ID to their info page
@app.route('/person/<int:person_id>')
def person(person_id):
    return redirect(url_for('person_info', person_id=person_id))

# Route for retrieving and displaying RDF data as HTML
@app.route('/person/<int:person_id>/info')
def person_info(person_id):
    # Build the URI for the person
    person_uri = W3ID[str(person_id)]

    # Query the RDF graph for properties of the person
    query = f"""
    SELECT ?property ?value WHERE {{
        <{person_uri}> ?property ?value .
    }}
    """

    # Execute the query
    rdf_data = []
    person_name = "Unknown Person"
    for row in g.query(query):
        prop = str(row.property)
        value = str(row.value)

        # Use the FOAF name as the title
        if prop == FOAF.name:
            person_name = value

        rdf_data.append((prop, value))

    # Render the HTML page with the RDF data
    return render_template_string(HTML_TEMPLATE, person_name=person_name, rdf_data=rdf_data)

if __name__ == '__main__':
    app.run(debug=True)
