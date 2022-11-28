from flask import Blueprint, request
from utils import run_query, get_engine, jwt_verification
from sqlalchemy import insert, Table, MetaData
categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

"""
id = id
title = category_name 
"""

@categories_bp.route("", methods=["POST"])
def create_category(): #DONE
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    categories = Table("categories", MetaData(bind=get_engine()), autoload=True)
    body = request.json
    category_name = body["category_name"]
    
    # run_query(f"INSERT INTO categories (title) VALUES {category_name}", commit=True)
    run_query(insert(categories).values({f"title":category_name}), commit=True)

    return {"message": "Category added"}, 200

@categories_bp.route("", methods=["GET"])
def get_category(): #DONE
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    data = run_query(f"SELECT * FROM categories")
    if len(data) < 1:
        return {"error" : "Category not found"}, 400
    else:
        return { "data:": data , "message": "Get category success"}, 200
        
@categories_bp.route("/<path:id>", methods=["PUT"])
def update_category(id): #DONE
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    
    body = request.json
    category_name = body["category_name"]
    data = run_query(f"SELECT FROM categories WHERE id={id}")
    if len(data) < 1:
        return{"message": "Category not found"}, 401
    else:
        run_query(f"UPDATE categories SET title = '{category_name}'\
                  WHERE id='{id}'", commit=True)
        return{"message": "Category updated"}, 200
        
@categories_bp.route("/<path:id>", methods=["DELETE"])
def soft_delete_category(id): #DONE
    token = str(request.headers.get('token'))
    verif = jwt_verification(token)
    if "message" in verif:
        return {"error": "User token expired, please re-login"}, 403
    data = run_query(f"SELECT FROM categories WHERE id='{id}'")
    if len(data)<1:
        return{"error": "Category not found"}, 401
    else:
        run_query(f"UPDATE categories SET soft_delete=True \
            WHERE id='{id}'", commit=True)
        return{"message": "Category deleted"}, 200
    
# @categories_bp.route("/hard/<path:id>", methods=["DELETE"])
# def hard_delete_category(id): #Tambahan Iseng
    
#     data = run_query(f"SELECT FROM categories WHERE id='{id}'")
#     if len(data)<1:
#         return{"error": "Category not found"}, 401
#     else:
#         run_query(f"DELETE FROM categories WHERE id='{id}'", commit=True)
#         return{"message": "Category deleted"}, 200
    
    

