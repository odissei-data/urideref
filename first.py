from flask import Flask, redirect, jsonify, url_for

app = Flask(__name__)

# Create a URI for a person resource
@app.route('/person/<int:person_id>')
def person(person_id):
    # If the resource is a concept or abstract entity, we use a 303 redirect
    return redirect(url_for('person_info', person_id=person_id))

# Create a page that describes the person (human-readable)
@app.route('/person/<int:person_id>/info')
def person_info(person_id):
    # You could generate this information dynamically (e.g., from a database)
    person_data = {
        1: {"name": "John Doe", "age": 30, "occupation": "Engineer"},
        2: {"name": "Jane Smith", "age": 25, "occupation": "Doctor"}
    }
    if person_id in person_data:
        return jsonify(person_data[person_id])
    else:
        return "Person not found", 404

if __name__ == '__main__':
    app.run(debug=True)
