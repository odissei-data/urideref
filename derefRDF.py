from flask import Flask, redirect, url_for, Response
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, DC

app = Flask(__name__)

# Define a custom namespace
EX = Namespace("http://example.com/")

# Create a URI for a person resource
@app.route('/person/<int:person_id>')
def person(person_id):
    # Redirect to the Turtle RDF description of the person
    return redirect(url_for('person_info', person_id=person_id))

# Create a page that returns the person description in RDF Turtle format
@app.route('/person/<int:person_id>/info')
def person_info(person_id):
    # RDF graph
    g = Graph()

    # Create a person resource URI based on the person_id
    person_uri = URIRef(f"http://example.com/person/{person_id}")

    # Sample person data
    person_data = {
        1: {"name": "John Doe", "age": 30, "occupation": "Engineer"},
        2: {"name": "Jane Smith", "age": 25, "occupation": "Doctor"}
    }

    # If the person exists, create RDF triples for them
    if person_id in person_data:
        person = person_data[person_id]
        # Add basic information using FOAF and custom properties
        g.add((person_uri, RDF.type, FOAF.Person))
        g.add((person_uri, FOAF.name, Literal(person["name"])))
        g.add((person_uri, EX.age, Literal(person["age"])))
        g.add((person_uri, EX.occupation, Literal(person["occupation"])))

        # Serialize the graph in Turtle format
        ttl_data = g.serialize(format='turtle')
        return Response(ttl_data, mimetype="text/turtle")
    else:
        return "Person not found", 404

if __name__ == '__main__':
    app.run(debug=True)
