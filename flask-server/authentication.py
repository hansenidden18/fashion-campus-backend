from flask import Blueprint, request
from utils import run_query
<<<<<<< HEAD

=======
>>>>>>> 23dada4616fef701b482e3ea695a8c43eb14945b
auth_bp = Blueprint("authentication", __name__, url_prefix="")

@auth_bp.route("/sign-up", methods=["POST"])
def sign_up():
    body = request.json
    
    name = body['name']
    email = body['email']
    phone_number = body['phone_number']
    password = body['password']

<<<<<<< HEAD
    data = run_query("SELECT nama FROM users")
    if data:
        usernames = [d['nama'] for d in data]
=======
    data = run_query("SELECT name FROM sers")
    if data:
        usernames = [d['username'] for d in data]
>>>>>>> 23dada4616fef701b482e3ea695a8c43eb14945b
    else:
        usernames = []

    if len(password) < 8:
        return {"error": "Password must contain at least 8 characters"}, 400
    if not any(char.isdigit() for char in password):
        return {"error": "Password must contain a number"}, 400

    if name in usernames:
        return {"error": f"Username {name} already exists"}, 409
<<<<<<< HEAD
    run_query(f"INSERT INTO users (nama, email, phone_number, password, balance) VALUES {name, email, phone_number,  password, 0}", commit=True)
    
    return {"message": "success, user created"}, 201

@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    body = request.json
    
    email = body['email']
    password = body['password']

    token = str(uuid.uuid4())

    data = run_query('SELECT * FROM users')
    if data:
        users = {d['username']:d['password'] for d in data}
    else:
        users = {}
    
    if (username not in users) or (users[username] != password):
        return {"error": "Username or password is incorrect"}, 401
    
    run_query(f"UPDATE users SET token = '{token}' WHERE username = '{username}'", commit=True)
    return {"message": "Welcome to the marketplace", "token": token}, 200
=======
    run_query(f"INSERT INTO users (username, password, type, balance) VALUES {username, password, types, 0}", commit=True)
    
    return {"message": "success, user created"}, 201
>>>>>>> 23dada4616fef701b482e3ea695a8c43eb14945b
