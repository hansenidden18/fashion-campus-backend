from flask import Blueprint, request
from fee_utils import regular_fee, next_fee
from utils import run_query, generate_jwt, jwt_verification, first
from flask_cors import CORS, cross_origin
from os.path import join
cart_bp = Blueprint("cart", __name__)
CORS(cart_bp)

@cart_bp.route("/cart", methods=["GET"])
def get_cart():

    token = str(request.headers.get('Authentication'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    data = run_query(f"SELECT * FROM cart WHERE customer_id = (SELECT id FROM users WHERE email='{verif['email']}' AND password='{verif['password']}')")
    if data:
        data = [{
                "id":d["id"],
                "details":{
                    "quantity":d["quantity"],
                    "size":d["size"]
                    },
                "price":d["price"],
                "image":join('/image/',d["image"]),
                "name":d["name"]} for d in data]
    else:
        data = []

    return {"data":data},200

@cart_bp.route("/user/shipping_address", methods=["GET"])
def get_shipping():

    token = str(request.headers.get('Authentication'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403

    user_id = first(f"SELECT id FROM users WHERE email='{verif['email']}' AND password='{verif['password']}'")
    data = run_query(f"SELECT * FROM user_address WHERE user_id={user_id['id']}")
    if data:
        data = [{"id": d["id"],
                "name": d["name"],
                "phone_number": d["phone_number"],
                "address": d["address"],
                "city": d["city"]} for d in data]
    else:
        data = []

    return {"data":data[0]},200

@cart_bp.route("/shipping_price", methods=["GET"])
def get_ship_price():
    token = str(request.headers.get('Authentication'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    user_id = first(f"SELECT id FROM users WHERE email='{verif['email']}' AND password='{verif['password']}'")
    data = run_query(f"SELECT * FROM cart WHERE customer_id= {user_id['id']}")
    if data:
        data = [d['price']*d['quantity'] for d in data]
    else:
        data = [0]
        name = first(f"SELECT nama FROM users WHERE id={user_id['id']}")
        # return {"message":f"user {name} doesn't have any cart yet"}, 400
    
    total_price  = sum(data)
    regular = regular_fee(total_price)
    next = next_fee(total_price)

    return {"data":[{
        "name":"regular",
        "price": regular
    },
    {
        "name":"next day",
        "price":next
    }]},200

@cart_bp.route("/order", methods=["POST"])
def create_order():
    token = str(request.headers.get('Authentication'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    body = request.json
    
    shipping_method = body['shipping_method']
    shipping_address = body['shipping_address']
    name = shipping_address["name"]
    phone_number = shipping_address["phone_number"]
    address = shipping_address["address"]
    city = shipping_address["city"]

    user_id = first(f"SELECT id FROM users WHERE token = '{token}'")
    data = run_query(f"SELECT * FROM cart WHERE customer_id = {user_id['id']}")
    if data:
        quantity = [d['quantity'] for d in data]
        size = [ d['size'] for d in data]
        product_id = [d['name'] for d in data]
        data = [d['price']*d['quantity'] for d in data]
    
    total_price  = sum(data)
    if shipping_method == "regular":
        price = regular_fee(total_price)
    else:
        price = next_fee(total_price)

    run_query(f'''INSERT INTO user_address(user_id, name, phone_number, address, city) VALUES {
        user_id['id'],
        name,
        phone_number,
        address,
        city
    }''',commit=True)

    address_id = run_query(f"SELECT id FROM user_address WHERE user_id= {user_id['id']} AND name = '{name}' AND address = '{address}' AND city = '{city}'")
    if address_id:
        ids = [ d["id"] for d in address_id]
    else:
        ids = None
    run_query(f'''INSERT INTO "order"(shipping, shipping_fee, status, total_price, customer_id, shipping_address, quantity, size, product) VALUES {
        shipping_method,
        price,
        "Processed",
        total_price,
        user_id['id'],
        ids[0],
        quantity[0],
        size[0][0],
        product_id[0]
        }''', commit=True)

    return {"message":"order success"}, 200

@cart_bp.route("/cart/<int:cart_id>", methods=["DELETE"])
def delete_cart(cart_id):

    token = str(request.headers.get('Authentication'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    run_query(f"DELETE FROM cart WHERE id = {cart_id}", commit=True)
    return {"message": "Cart deleted"}, 200
