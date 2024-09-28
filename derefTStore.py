from flask import Flask, redirect, url_for, Response
from SPARQLWrapper import SPARQLWrapper, TURTLE
from rdflib import Graph, URIRef

app = Flask(__name__)

# Configure your SPARQL endpoint (triple store)
SPARQL_ENDPOINT = "http://localhost:7200/repositories/my-repo"

# Create a URI for a person resource
@app.route('/person/<int:person_id>')
def person(person_id):
    # Redirect to the Turtle RDF description of the person
    return redirect(url_for('person_info', person_id=person_id))

# Query the triple store and return the RDF data in Turtle format
@app.route('/person/<int:person_id>/info')
def person_info(person_id):
    # Construct the URI for the person resource
    person_uri = f"http://example.com/person/{person_id}"

    # Define the SPARQL query to retrieve the person's data
    query = f"""
    PREFIX ex: <http://example.com/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    CONSTRUCT {{
        <{person_uri}> a foaf:Person ;
                       foaf:name ?name ;
                       ex:age ?age ;
                       ex:occupation ?occupation .
    }}
    WHERE {{
        <{person_uri}> foaf:name ?name ;
                       ex:age ?age ;
                       ex:occupation ?occupation .
    }}
    """

    # Query the triple store using SPARQLWrapper
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(TURTLE)
    
    try:
        # Get the Turtle RDF data from the triple store
        results = sparql.query().convert()

        # Return the Turtle data as the response
        return Response(results, mimetype="text/turtle")

    except Exception as e:
        return f"Error querying triple store: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
