from flask import Blueprint, request
from utils import run_query, jwt_verification

profile_bp = Blueprint("profile", __name__, url_prefix="")

# USER
@profile_bp.route("/user", methods=["GET"])
def get_user():
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403

    data = run_query(f"SELECT nama, email, phone_number FROM users WHERE token = '{token}'")
    if data:
        data = [{
                "name":d["nama"],
                "email":d["email"],
                "phone_number":d["phone_number"]} for d in data ]
    else:
        data = []

    return data[0],200

#USER SHIPPING_ADDRESS
@profile_bp.route("/user/shipping_address", methods=["POST"])
def shipping_address():
    
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403

    body = request.json
    
    name = body['name']
    phone_number = body['phone_number']
    address = body['address']
    city = body['city']
    
    data = run_query(f"SELECT address FROM user_address WHERE user_id = (SELECT id FROM users WHERE token = '{token}') AND address = '{address}'")
    if data:
        run_query(f"UPDATE user_address SET name = '{name}', phone_number = {phone_number}, address = {address}, city = {city} WHERE user_id = (SELECT id FROM users WHERE token = '{token}')")
    else:
        run_query(f"INSERT INTO user_address (user_id, name, phone_number, address, city) VALUES (SELECT id FROM users WHERE nama = '{name}'),{name, phone_number,  address, city }", commit=True)
    
    return {"message": "address successfully changed"}, 200

#USER TOP UP BALANCE
@profile_bp.route("/user/balance", methods=["POST"])
def top_up_balance():

    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    body = request.json
    
    amount = int(body['amount'])

    if amount <= 0:
        return {"message": "Amount must be a positive integer"}, 400

    data = run_query(f"SELECT balance FROM users WHERE token = '{token}'")
    if data:
        data = [d['balance'] for d in data]
    else:
        data = [0]
    
    new_balance = data[0] + amount
    run_query(f"UPDATE users SET balance = {new_balance} WHERE token = '{token}'")
    
    return {"message": "balance topped-up successfully"}, 200

#USER BALANCE
@profile_bp.route("/user/balance", methods=["GET"])
def balance():

    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    data = run_query(f"SELECT balance FROM users WHERE token = '{token}'")
    if data:
        data = [{
                "balance":d["balance"]} for d in data]
    else:
        data = []

    return data[0],200


# USER ORDER
@profile_bp.route("/user/order", methods=["GET"])
def get_order():
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403

    users = run_query(f"SELECT id FROM users WHERE token = '{token}'")
    if users:
        user = [d['id'] for d in users]
    else:
        return {"message": "Unauthorized user"}, 401
    
    orders = run_query(f"SELECT * FROM order WHERE customer_id = {user[0]} ORDER BY time_created DESC")
    
    order_items = {}
    order_address = {}
    for order in orders:
        items = run_query(f'''
                            SELECT  order.product
                                    product.price,
                                    order.quantity,
                                    order.size,
                                    product.image_url,
                                    product.title FROM orders
                            JOIN (SELECT product.id, product.price, product.image_url, product.title FROM product) AS prod ON prod.id = order.product
                            WHERE order.id == {order["id"]}
        ''')

        order_items[order["id"]] = [
            {
                'id': item["product"],
                'details': {
                    'quantity': item["quantity"],
                    'size': item["size"]
                },
                'price': item["price"],
                'image': item["image_url"],
                'name': item["title"]
            } for item in items
        ]

        shipping_address = run_query(f"SELECT * FROM user_address WHERE id = {order['shipping_address']}")

        for address in shipping_address:
            order_address[order["id"]] = {
                "name": address["name"],
                "phone_number": address["phone_number"],
                "address": address["address"],
                "city": address["city"]
            }


    return {
        'data': [
            {
                'id': order["id"],
                'created_at': order["time_created"],
                'products': order_items[order["id"]],
                'shipping_method': order["shipping"],
                'shipping_address': order_address[order["id"]]
            } for order in orders
        ]
    },200
