from flask import Flask, redirect, url_for, render_template_string
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef

app = Flask(__name__)

# Configure your SPARQL endpoint (triple store)
SPARQL_ENDPOINT = "http://localhost:7200/repositories/my-repo"

# W3ID base URI
W3ID_BASE_URI = "https://w3id.org/example/person/"

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

# Create a URI for a person resource using W3ID
@app.route('/person/<int:person_id>')
def person(person_id):
    # Redirect to the HTML RDF description of the person
    return redirect(url_for('person_info', person_id=person_id))

# Query the triple store and return the RDF data as HTML (like DBpedia)
@app.route('/person/<int:person_id>/info')
def person_info(person_id):
    # Construct the W3ID URI for the person resource
    person_uri = f"{W3ID_BASE_URI}{person_id}"

    # Define the SPARQL query to retrieve the person's data
    query = f"""
    PREFIX ex: <http://example.com/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT ?property ?value
    WHERE {{
        <{person_uri}> ?property ?value .
    }}
    """

    # Query the triple store using SPARQLWrapper
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        # Execute the query and get the results in JSON format
        results = sparql.query().convert()

        # Extract RDF triples and format them as property-value pairs
        rdf_data = []
        person_name = "Unknown Person"
        
        for result in results["results"]["bindings"]:
            prop = result["property"]["value"]
            value = result["value"]["value"]

            # Display the name as the title if found in FOAF:name
            if "foaf/name" in prop:
                person_name = value

            rdf_data.append((prop, value))

        # Render the HTML using the extracted data
        return render_template_string(HTML_TEMPLATE, person_name=person_name, rdf_data=rdf_data)

    except Exception as e:
        return f"Error querying triple store: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
