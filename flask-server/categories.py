from flask import Blueprint, request
from utils import run_query, get_engine, jwt_verification
from sqlalchemy import insert, Table, MetaData
from flask_cors import CORS

categories_bp = Blueprint("categories", __name__)
CORS(categories_bp)

"""
id = id
title = category_name 
"""

# @categories_bp.route("", methods=["POST"])
# def create_category(): #DONE
#     token = str(request.headers.get('Authenticaion'))
#     verif = jwt_verification(token)
#     if "message" in verif:
#         return {"error": "User token expired, please re-login"}, 403
    
#     categories = Table("categories", MetaData(bind=get_engine()), autoload=True)
#     body = request.json
#     category_name = body["category_name"]
    
#     # run_query(f"INSERT INTO categories (title) VALUES {category_name}", commit=True)
#     run_query(insert(categories).values({f"title":category_name}), commit=True)

#     return {"message": "Category added"}, 200

@categories_bp.route("/categories", methods=["GET"])
def get_category():

    data = run_query(f"SELECT * FROM categories")
    if len(data) < 1:
        return {"error" : "Category not found"}, 400
    else:
        data = [{
            "id": d["id"],
            "title": d["title"]
        } for d in data]
        return {"data": data}, 200
        
@categories_bp.route("/categories/<int:id>", methods=["PUT"])
def update_category(id): #DONE
    body = request.json
    category_name = body["category_name"]
    data = run_query(f"SELECT FROM categories WHERE id={id}")
    if len(data) < 1:
        return{"message": "Category not found"}, 401
    else:
        run_query(f"UPDATE categories SET title = '{category_name}'\
                WHERE id='{id}'", commit=True)
        return{"message": "Category updated"}, 200
        
@categories_bp.route("/categories/<int:id>", methods=["DELETE"])
def soft_delete_category(id): 
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
    
    

