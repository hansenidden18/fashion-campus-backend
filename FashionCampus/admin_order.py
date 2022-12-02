from flask import Blueprint, request
from utils import run_query, admin_token_checker
from sqlalchemy import insert, Table, MetaData
from flask_cors import CORS
admin_order_bp = Blueprint("admin_order", __name__)
CORS(admin_order_bp)

@admin_order_bp.route("/orders", methods = ["GET"])
def admin_get_orders():
    token = str(request.headers.get('Authentication'))
    # admin_token_checker(token)
    
    param = request.args
    params = param.get
    sort_by = params("sort_by", default = "price a_z", type=str)
    page = params ("page", default = 1, type=int)
    page_size = params("page_size", default=100, type=int)

    if sort_by.lower() == "price a_z":
        sort_by = "ASC"
    elif sort_by.lower() == "price z_a":
        sort_by = "DESC"
    
    offset = (page - 1) * page_size
    
    data = run_query(f'''SELECT o.id, u.nama as user_name, to_char(o.time_created,'Day, DD month YYYY') as created_at, \
                        o.customer_id as user_id, u.email as user_email, o.total_price as total \
                        FROM "order" o LEFT JOIN users u \
                        ON o.customer_id = u.id \
                        ORDER BY total {sort_by} OFFSET {offset} LIMIT {page_size}''')
    if len(data) < 1:
        return {"error": "User orders not found"}, 400
    else:
        data = [{
            "id": x["id"],
            "user_name": x["user_name"],
            "created_at": x["created_at"],
            "user_id": x["user_id"],
            "user_email": x["user_email"],
            "total" : x["total"]
        }for x in data]
        return {"data": data}, 200
    