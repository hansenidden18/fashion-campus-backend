from flask import Blueprint, request
from utils import get_engine, run_query, admin_token_checker, user_token_checker
from sqlalchemy import insert, Table, MetaData
admin_product_bp = Blueprint("adminproduct",__name__,url_prefix="/products")


"""
TABLE PRODUCT
id = id/product_id
title = product_name
brand_name = product_name
size
product_detail = description
image_url = images
condition = condition
price = price
categories_id = category
"""


@admin_product_bp.route("", methods=["POST"])
def create_product(): #ADMIN
    product = Table("product", MetaData(bind=get_engine()), autoload=True)
    token = str(request.headers.get('token'))
    admin_token_checker(token)
 
    body = request.json 
    product_name = body["product_name"]
    description = body["description"]
    images = body["image_url"]
    condition = body["condition"]
    category = body["categories_id"]
    price = body["price"]
    
    run_query(insert(product).values({f"brand_name":product_name, "product_detail":description, "image_url":images, \
        "condition":condition, "categories_id":category, "price":price, "soft_delete":False}), commit=True)
    return {"message": "Product added"}, 200

@admin_product_bp.route("", methods=["PUT"])
def update_product(): #ADMIN
    token = str(request.headers.get('token'))
    admin_token_checker(token)
            
    body=request.json
    product_name = body["product_name"]
    description = body["description"]
    images = body["image_url"]
    condition = body["condition"]
    category = body["categories_id"]
    price = body["price"]
    product_id = body["product_id"]
    
    data = run_query(f"SELECT from product WHERE id={product_id}")
    if len(data) < 1:
        return {"error": "Product id not found"}, 401
    else:
        run_query(f"UPDATE product SET brand_name = '{product_name}', product_detail = '{description}', image_url='{images}',\
            condition = '{condition}', categories_id = '{category}', price = '{price}', id = '{product_id}' WHERE id='{product_id}'", commit=True)
        return{"message" : "Product updated"}, 200

@admin_product_bp.route("/<path:id>", methods=["DELETE"])
def soft_delete_product(id): #ADMIN
    token = str(request.headers.get('token'))
    admin_token_checker(token)
    
    data = run_query(f"SELECT from product WHERE id={id}")
    if len(data) < 1:
        return {"error": "Product id not found"}, 401
    else:
        run_query(f"UPDATE product SET soft_delete=True \
        WHERE id={id}", commit=True)
        return {"message": "Product deleted"}, 200
