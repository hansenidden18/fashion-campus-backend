from flask import Blueprint, request
from utils import get_engine, run_query, admin_token_checker, user_token_checker
from sqlalchemy import insert, Table, MetaData
from flask_cors import CORS
from os.path import join, dirname, realpath
import base64

admin_product_bp = Blueprint("adminproduct",__name__)
CORS(admin_product_bp)

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


@admin_product_bp.route("/products", methods=["POST"])
def create_product(): #ADMIN
    product = Table("product", MetaData(bind=get_engine()), autoload=True)
    token = str(request.headers.get('Authentication'))
    # admin_token_checker(token)

    body = request.json 
    product_name = body["product_name"]
    description = body["description"]
    images = body["images"]
    condition = body["condition"]
    category = body["category"]
    price = body["price"]
    
    paths = join(dirname(realpath(__file__)), 'static/')
    new_image = []
    i = 1
    for image in images:
        if 'data' in image[0:4]:
            head,tail = image.split(';')
            _,ext = head.split('/')
            _,msg = tail.split(',')
            name_product = product_name.replace(" ","_")

            with open(join(paths, name_product+ str(i) +"."+ext), "wb") as fh:
                fh.write(base64.b64decode(msg))
            new_image.append(name_product+ str(i) +"."+ext)
            i+=1
        else:
            _,_,tail = image.split('/')
            new_image.append(tail)
    run_query(insert(product).values({f"title":product_name, "product_detail":description, "image_url":new_image, \
        "condition":condition, "categories_id":category, "price":price, "soft_delete":False}), commit=True)
    return {"message": "Product added"}, 200

@admin_product_bp.route("/products", methods=["PUT"])
def update_product(): #ADMIN
    product = Table("product", MetaData(bind=get_engine()), autoload=True)
    token = str(request.headers.get('Authentication'))
            
    body=request.json
    product_name = body["product_name"]
    description = body["description"]
    images = body["images"]
    condition = body["condition"]
    category = body["category"]
    price = body["price"]
    product_id = body["product_id"]
    
    paths = join(dirname(realpath(__file__)), 'static/')
    new_image = []
    i = 1
    for image in images:
        if 'data' in image[0:4]:
            head,tail = image.split(';')
            _,ext = head.split('/')
            _,msg = tail.split(',')
            name_product = product_name.replace(" ","_")

            with open(join(paths, name_product+ str(i) +"."+ext), "wb") as fh:
                fh.write(base64.b64decode(msg))
            new_image.append(name_product+ str(i) +"."+ext)
            i+=1
        else:
            _,_,tail = image.split('/')
            new_image.append(tail)

    data = run_query(f"SELECT from product WHERE id={product_id}")
    if len(data) < 1:
        return {"error": "Product id not found"}, 401
    else:
        run_query(product.update().where(product.c.id==product_id).values({f"title":product_name, "product_detail":description, "image_url":new_image, \
        "condition":condition, "categories_id":category, "price":price}), commit=True)
        return{"message" : "Product updated"}, 200

@admin_product_bp.route("/products/<path:id>", methods=["DELETE"])
def soft_delete_product(id): #ADMIN
    token = str(request.headers.get('Authentication'))
    # admin_token_checker(token)
    
    data = run_query(f"SELECT from product WHERE id={id}")
    if len(data) < 1:
        return {"error": "Product id not found"}, 401
    else:
        run_query(f"DELETE FROM product WHERE id={id}", commit=True)
        return {"message": "Product deleted"}, 200