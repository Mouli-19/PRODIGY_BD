from flask import Flask, request, jsonify
from uuid import uuid4
import re

app = Flask(_name_)
users = {}  # In-memory storage

# Email validation regex
EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Create user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    age = data.get("age")

    if not name or not email or not age:
        return jsonify({"error": "Missing required fields"}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"error": "Invalid email"}), 400

    user_id = str(uuid4())
    users[user_id] = {"id": user_id, "name": name, "email": email, "age": age}
    return jsonify(users[user_id]), 201

# Read user
@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# Update user
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    name = data.get("name", user["name"])
    email = data.get("email", user["email"])
    age = data.get("age", user["age"])

    if email and not EMAIL_REGEX.match(email):
        return jsonify({"error": "Invalid email"}), 400

    users[user_id].update({"name": name, "email": email, "age": age})
    return jsonify(users[user_id])

# Delete user
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

# List users (optional)
@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(users.values()))
