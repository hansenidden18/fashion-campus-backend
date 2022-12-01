from flask import Blueprint, request
from utils import get_engine, run_query, admin_token_checker, user_token_checker
from sqlalchemy import insert, Table, MetaData

admin_sales_bp = Blueprint("admin", __name__)

@admin_sales_bp.route("/sales", methods=["GET"])
def get_total_sales():  #DONE
    product = Table("product", MetaData(bind=get_engine()), autoload=True)
    token = str(request.headers.get('Authentication'))
    # admin_token_checker(token)
    
    data = run_query(f"SELECT balance as total FROM users \
                        WHERE type='seller'")
    data = [d['balance'] for d in data]
    return { "data": data[0] }, 200   
