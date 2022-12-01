from flask import Blueprint, request
from utils import get_engine, jwt_verification, run_query, admin_token_checker, user_token_checker
from sqlalchemy import insert, Table, MetaData
from flask_cors import CORS
from os.path import join

product_bp = Blueprint("product",__name__)
CORS(product_bp)

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

@product_bp.route("/products", methods=["GET"])
def getproduct_list():
    token = str(request.headers.get('Authentication'))
    if admin_token_checker(token):
        data = run_query(f"SELECT id, image_url AS image, title, price FROM product")
        if len(data) < 1:
            return {"error": "Product not found"}, 400
        else:
            data = [{
                "id": d["id"],
                "image": [join('/image/',d) for d in d['image']],
                "title": d["title"],
                "price": d["price"]
            }for d in data]
        return {"data": data, "total_rows" : len(data)}, 200
    
    param = request.args
    params = param.get
    page = params("page", type=int)
    page_size = params("page_size", type=int)
    sort_by = params("sort_by", type=str)
    category = params("category", type=int)
    price = params("price", type=int) or 1000000
    condition = params("condition", type=str)
    product_name = params("product_name", type=str)
    
    if sort_by.lower() == "price a_z":
        sort = "ASC"
    elif sort_by.lower() == "price z_a":
        sort = "DESC"
    else:
        sort = "ASC"
        return {"error" : "sort_by must be 'price_a_z' or 'price_z_a'!"}, 400
    offset = page * page_size
    verif = run_query(f'SELECT * FROM product')
    if len(verif) >= 1:
        offset = 0
    if not condition and not product_name and not category:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE price <= {price} \
                            ORDER BY price {sort} OFFSET {offset} LIMIT {page_size}")
    elif not condition and not category:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE categories_id='{category}' \
                            AND title='{product_name}' AND price <= {price} \
                            ORDER BY price {sort} OFFSET {offset} LIMIT {page_size}")
    elif not product_name and not category:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE categories_id='{category}' \
                            AND condition='{condition}' AND price <= {price} \
                            ORDER BY price {sort} OFFSET {offset} LIMIT {page_size}")
    elif not product_name and not condition:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE categories_id='{category}' \
                            AND price <= {price} \
                            ORDER BY price {sort} OFFSET {offset} LIMIT {page_size}")
    elif not condition:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE title='{product_name}' \
                            AND categories_id='{category}' AND price <= {price} \
                            ORDER BY price {sort} OFFSET {offset} LIMIT {page_size}")
    elif not product_name:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE categories_id='{category}' \
                            AND condition='{condition}' AND price <= {price} \
                            ORDER BY price {sort} OFFSET {offset} LIMIT {page_size}")
    elif not category:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE title='{product_name}' \
                            AND condition='{condition}' AND price <= {price} \
                            ORDER BY price {sort} OFFSET {offset} LIMIT {page_size}")
    else:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE title='{product_name}' AND categories_id='{category}' \
                            AND condition='{condition}' AND price <= {price} \
                            ORDER BY price {sort} OFFSET {offset} LIMIT {page_size}")
    if len(data) < 1:
        return {"error": "Product not found"}, 400
    else:
        data = [{
            "id": d["id"],
            "image": [join('/image/',d) for d in d['image']],
            "title": d["title"],
            "price": d["price"]
        }for d in data]
        return {"data": data, "total_rows" : len(data)}, 200

@product_bp.route("/products/<int:id>", methods=["GET"])
def getproducts_detail(id):
    data = run_query(f"SELECT p.id, p.title, p.brand_name, p.size, p.product_detail, p.price, p.image_url, \
        p.categories_id AS category_id, c.title AS category_name FROM product p \
        RIGHT JOIN categories c ON p.categories_id = c.id \
        WHERE p.id={id} ")
    if len(data) < 1:
        return {"error": "Product not found"}, 400
    else:
        data = [{
            "id": d["id"],
            "title": d["title"],
            "size": d["size"],
            "product_detail": d["product_detail"],
            "price": d["price"],
            "images_url": [join('/image/', d["image_url"])],
            "category_id": d["category_id"],
            "category_name":d["category_name"]
        } for d in data]
        return { "data": data[0] }, 200
    
# @product_bp.route("/search_image", methods=["POST"])
# def search_product():  #TUNGGU TIM AI
#     body = request.json
#     images = body["image"]
    
#     data = run_query(f"SELECT categories_id \
#         FROM product \
#         WHERE image_url = '{images}'")
#     if len(data) < 1:
#         return{"error": "Images not found"}, 400
#     else:
#         return {"data": data, "message":"Search product success"}, 200