from flask import Blueprint, request
from utils import run_query, get_engine, jwt_verification, admin_token_checker
from sqlalchemy import insert, Table, MetaData
categories_bp = Blueprint("categories", __name__, url_prefix="/categories")

"""
id = id
title = category_name 
"""

@categories_bp.route("", methods=["POST"])
def create_category(): #DONE
    token = str(request.headers.get('token'))
    admin_token_checker(token)
    categories = Table("categories", MetaData(bind=get_engine()), autoload=True)
    
    body = request.json
    category_name = body["category_name"]
    
    run_query(insert(categories).values({f"title":category_name}), commit=True)

    return {"message": "Category added"}, 200

@categories_bp.route("", methods=["GET"])
def get_category(): #BISA USER ATAU ADMIN
    token = str(request.headers.get('token'))
    
    if admin_token_checker(token):
        data = run_query(f"SELECT * FROM categories")
        if len(data) < 1:
            return {"error" : "Category not found"}, 400
        else:
            data = [{
                "id": d["id"],
                "title": d["title"]
            } for d in data]
            return {"data": data}, 200
    else:
        data = run_query(f"SELECT * FROM categories WHERE soft_delete != True")
        if len(data) < 1:
            return {"error" : "Category not found"}, 400
        else:
            data = [{
                "id": d["id"],
                "title": d["title"]
            } for d in data]
            return {"data": data}, 200
        
        
@categories_bp.route("/<path:id>", methods=["PUT"])
def update_category(id): #DONE
    token = str(request.headers.get('token'))
    admin_token_checker(token)
    
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
    admin_token_checker(token)
    
    data = run_query(f"SELECT FROM categories WHERE id='{id}'")
    if len(data)<1:
        return{"error": "Category not found"}, 401
    else:
        run_query(f"UPDATE categories SET soft_delete=True \
            WHERE id='{id}'", commit=True)
        return{"message": "Category deleted"}, 200
