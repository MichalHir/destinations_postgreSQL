from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
# Create an instance of the Flask class
app = Flask(__name__)


# Initialize CORS
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500","https://petshop-front-1bmj.onrender.com"]}})
# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="pets_db_b5de",
        user="pets_db_b5de_user",
        password="vYXeDGUTqlWrRPo89S7GvNnwvkRRlO4B",
        host="dpg-cr889qlsvqrc73dr1dkg-a.oregon-postgres.render.com",
        port="5432",
        cursor_factory=RealDictCursor,  # Use RealDictCursor to get dict results
    )
    return conn


@app.route("/")
def root():
    return """
    GET/pets - list of pets <br>
    GET/pets/<id> - single pet <br>
    POST/pets - add a pet <br>
    DELETE/pets/<id> - delete a pet <br>
    PUT/pets/<id> - update a pet
    """


# Get list of pets
@app.route("/pets")
def pets_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, image FROM pets;")
    pets = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(pets)


# Add a new pet
@app.route("/pets", methods=["POST"])
def add_pet():
    new_pet = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pets (name, age, image) VALUES (%s, %s, %s)",
        (new_pet["name"], new_pet["age"], new_pet["image"]),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"result": "Added successfully"}), 201


# Get a single pet by ID
@app.route("/pets/<int:id>/")
def single_pet(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, image FROM pets WHERE id = %s;", (id,))
    pet = cursor.fetchone()
    cursor.close()
    conn.close()

    if pet is None:
        return jsonify({"result": "Pet not found"}), 404

    return jsonify(pet)


# Delete a pet by ID
@app.route("/pets/<int:id>", methods=["DELETE"])
def delete_pet(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pets WHERE id = %s;", (id,))
    conn.commit()
    rowcount = cursor.rowcount
    cursor.close()
    conn.close()

    if rowcount == 0:
        return jsonify({"result": "Pet not found"}), 404

    return jsonify({"result": "Pet deleted successfully"}), 200


# Update a pet by ID
@app.route("/pets/<int:id>", methods=["PUT"])
def update_pet(id):
    updated_pet = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE pets SET name = %s, age = %s, image = %s WHERE id = %s;",
        (updated_pet["name"], updated_pet["age"], updated_pet["image"], id),
    )
    conn.commit()
    rowcount = cursor.rowcount
    cursor.close()
    conn.close()

    if rowcount == 0:
        return jsonify({"result": "Pet not found"}), 404

    return jsonify({"result": "Pet updated successfully"}), 200


# Run the app only if this script is executed (not imported)
if __name__ == "__main__":
    app.run(debug=True)
