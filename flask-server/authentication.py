from flask import Blueprint, request
from utils import run_query, generate_jwt, jwt_verification
from datetime import datetime, timedelta
import jwt
auth_bp = Blueprint("authentication", __name__)

@auth_bp.route("/sign-up", methods=["POST"])
def sign_up():
    body = request.json
    
    name = body['name']
    email = body['email']
    phone_number = body['phone_number']
    password = body['password']

    data = run_query("SELECT nama,email FROM users")
    if data:
        usernames = {d['nama']:d['email'] for d in data}
    else:
        usernames = {}

    if len(password) < 8:
        return {"error": "Password must contain at least 8 characters"}, 400
    if not any(char.isdigit() for char in password):
        return {"error": "Password must contain a number"}, 400

    if name in usernames:
        return {"error": f"Username {name} already exists"}, 409
    if email in usernames.values():
        return {"error": f"Username {email} already exists"}, 409
    run_query(f"INSERT INTO users (nama, email, phone_number, password, balance) VALUES {name, email, phone_number,  password, 0}", commit=True)
    
    return {"message": "success, user created"}, 201

@auth_bp.route("/sign-in", methods=["POST"])
def sign_in():
    body = request.json
    
    email = body['email']
    password = body['password']

    data = run_query('SELECT email, password FROM users')
    if data:
        users = {d['email']:d['password'] for d in data}
    else:
        users = {}
    
    if (email not in users) or (users[email] != password):
        return {"error": "Email or password is incorrect"}, 401
    
    user = run_query(f"SELECT * from users WHERE email = '{email}'")
    if user:
        user_token = [d['token'] for d in user]
        user = [[d["nama"],d["token"], d["phone_number"]] for d in user]
        
    if user_token[0]:
        try:
            decoded_token = jwt_verification(user_token[0])
            print(decoded_token)
        except:
            run_query(f"UPDATE users SET token = NULL WHERE nama = '{user[0][0]}' AND email = '{email}'", commit=True)
            return {"error": "Token error re-login please"}, 400
        # if decoded_token['exp'] - (datetime.now() + timedelta(days=1)) >= timedelta(seconds=1):
        #     run_query(f"UPDATE users SET token = NULL WHERE nama = '{user[0][0]}' AND email = '{email}'", commit=True)
        #     return {"error": "Token already expired re-login please"}, 400
        

    token = {'email': email, 'password': password}
    token = generate_jwt(token)

    run_query(f"UPDATE users SET token = '{token}' WHERE email = '{email}' AND password = '{password}'", commit=True)
    return {
            "user_information":{
                "name": user[0][0],
                "email": email,
                "phone_number": user[0][2],
                "type": "buyer"
            },
            "token": token,
            "message": "Login success"
        }, 200
