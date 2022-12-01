from flask import Blueprint, request
from utils import get_engine, jwt_verification, run_query, admin_token_checker, user_token_checker
from sqlalchemy import insert, Table, MetaData
test_bp = Blueprint("test",__name__,url_prefix="/")

@test_bp.route("/products/iseng", methods=["GET"])
def getproductss(): # Ini iseng doang buat ngeliat hasil create 
    data = run_query(f"SELECT id, brand_name, product_detail, image_url, condition, categories_id, price, soft_delete  FROM product")
    if len(data) < 1:
        return {"error": "Product not found"}, 400
    else:
        return { "data:": data }, 200
    
@test_bp.route("/products/hard/<path:id>", methods=["DELETE"])
def hard_delete_product(id): #ISENG
    data = run_query(f"SELECT from product WHERE id={id}")
    if len(data) < 1:
        return {"error": "Product id not found"}, 401
    else:
        run_query(f"DELETE FROM product WHERE id={id}", commit=True)
        return {"message": "Product deleted"}, 200
    
@test_bp.route("/categories/hard/<path:id>", methods=["DELETE"])
def hard_delete_category(id): #Tambahan Iseng
    
    data = run_query(f"SELECT FROM categories WHERE id='{id}'")
    if len(data)<1:
        return{"error": "Category not found"}, 401
    else:
        run_query(f"DELETE FROM categories WHERE id='{id}'", commit=True)
        return{"message": "Category deleted"}, 200
    
