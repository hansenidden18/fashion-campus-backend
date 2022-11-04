from flask import Blueprint, request
from utils import run_query
auth_bp = Blueprint("authentication", __name__, url_prefix="")

@auth_bp.route("/sign-up", methods=["POST"])
def add_user():
    body = request.json

    name = body['name']
    email = body['email']
    phone_number = body['phone_number']
    password = body['password']

    data = run_query("SELECT name FROM sers")
    if data:
        usernames = [d['username'] for d in data]
    else:
        usernames = []

    if len(password) < 8:
        return {"error": "Password must contain at least 8 characters"}, 400
    if not any(char.isdigit() for char in password):
        return {"error": "Password must contain a number"}, 400

    if name in usernames:
        return {"error": f"Username {name} already exists"}, 409
    run_query(f"INSERT INTO users (username, password, type, balance) VALUES {username, password, types, 0}", commit=True)
    
    return {"message": "success, user created"}, 201