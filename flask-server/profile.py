from flask import Blueprint, request
from utils import run_query, jwt_verification

profile_bp = Blueprint("profile", __name__, url_prefix="")

# Contoh
@profile_bp.route("/user", methods=["GET"])
def add_profile():
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403

    data = run_query(f"SELECT nama, email, phone_number FROM users")
    if data:
        data = {"data":[{
                "nama":d["nama"],
                "email":d["email"],
                "phone_number":d["phone_number"]} for d in data]}
    else:
        data = []

    return data,200

@profile_bp.route("/user/shipping_address", methods=["POST"])
def shipping_address():

    body = request.json
    
    name = body['name']
    phone_number = body['phone_number']
    address = body['address']
    city = body['city']

    data = run_query("SELECT users.nama, users.phone_number FROM user JOIN user_address on id GROUP BY user_address.address, user_address.city")
    if data:
        usernames = {d['nama']:d['phone_number']for d in data}
    else:
        usernames = {}
    if data:
        usernames = {d['address']:d['city']for d in data}
    else:
        usernames = {}
    if name in usernames:
        return {"error": f"Username {name} already exists"}, 409
    if phone_number in usernames.values():
        return {"error": f"Username {phone_number} already exists"}, 409
    run_query(f"INSERT INTO users (nama,phone_number, address, city) VALUES {name, phone_number,  address, city }", commit=True)
    
    return {"message": "success, user created"}, 201

@profile_bp.route("/user/balance", methods=["POST"])
def top_up_balance():

    body = request.json
    
    amount = body['total_price']

    data = run_query("SELECT total_price FROM order")
    if data:
        usernames = {d['total_price'] for d in data}
    else:
        usernames = {}
    if amount in usernames:
        return {"error": f"Username {amount} already exists"}, 409
    run_query(f"INSERT INTO order (total_price) VALUES {amount}", commit=True)
    
    return {"message": "success, user created"}, 201

@profile_bp.route("/user/balance", methods=["GET"])
def balance():
    token = str(request.headers.get('token'))
    if "message" in token:
        return {"error": "User token expired, please re-login"}, 403
        
    data = run_query(f"SELECT balance FROM users")
    if data:
        data = {"data":[{
                "balance":d["balance"]} for d in data]}
    else:
        data = []

    return data,200


# Contoh
@profile_bp.route("/user/order", methods=["GET"])
def add_order():
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403

    data = run_query(f"SELECT order.id, order.time_created FROM order JOIN cart on id GROUP BY cart.id, cart.size, cart.price, cart.image, cart.name JOIN user_address on id GROUP BY user_address.name, user_address.phone_number, user_address.address, user_address.city")
    if data:
        data = {"data":[{
                "id":d["id"],
                "create_at":d["time_created"],}],
                    "product":[
                        {
                            "id":d["id"],
                            "size":d["size"],
                            "quantity":d["quantity"],
                            "price":d["price"],
                            "image":d["image"],
                            "name":d["brand_name"],}],
                "shipping_method":d["shipping"],
                "shipping_address":[
                        {
                            "name":d["name"],
                            "phone_number":d["phone_number"],
                            "address":d["address"],
                            "city":d["city"],}],}
    else:
        data = []

    return data,200
