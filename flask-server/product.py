from flask import Blueprint, request
from utils import get_engine, jwt_verification, run_query, admin_token_checker, user_token_checker
from sqlalchemy import insert, Table, MetaData
from os.path import join
product_bp = Blueprint("product",__name__,url_prefix="/products")
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

"""
getproductlist()
TODO
- Dibuat menjadi admin and umum, kalau admin soft_delete ditampilkan, umum tidak
- Page dan page size adalah halaman beserta isi dari halaman
"""
# @product_bp.route("", methods=["GET"])
# def getproduct_list(): #harusnya admin and umum. kalau admin soft_delete true
#     param = request.args
#     params = param.get
#     page = params("page", type=int)
#     page_size = params("page_size", type=int)
#     sort_by = params("sort_by", type=str)
#     category = params("category", type=int)
#     price = params("price", type=int) or 1000000
#     condition = params("condition", type=str)
#     product_name = params("product_name", type=str)
    
#     if sort_by.lower() == "price a_z":
#         sort = "ASC"
#     elif sort_by.lower() == "price z_a":
#         sort = "DESC"
#     else:
#         sort = "ASC"
#         return {"error" : "sort_by must be 'price_a_z' or 'price_z_a'!"}, 400
#     if not page_size:
#         page_size = 100
#     if not condition and not product_name and not category:
#         data = run_query(f"SELECT id, image_url AS image, title, price \
#                             FROM product WHERE price <= {price} \
#                             ORDER BY price {sort} LIMIT {page_size}")
#     elif not condition and not category:
#         data = run_query(f"SELECT id, image_url AS image, title, price \
#                             FROM product WHERE categories_id='{category}' \
#                             AND title='{product_name}' AND price <= {price} \
#                             ORDER BY price {sort} LIMIT {page_size}")
#     elif not product_name and not category:
#         data = run_query(f"SELECT id, image_url AS image, title, price \
#                             FROM product WHERE categories_id='{category}' \
#                             AND condition='{condition}' AND price <= {price} \
#                             ORDER BY price {sort} LIMIT {page_size}")
#     elif not product_name and not condition:
#         data = run_query(f"SELECT id, image_url AS image, title, price \
#                             FROM product WHERE categories_id='{category}' \
#                             AND price <= {price} \
#                             ORDER BY price {sort} LIMIT {page_size}")
#     elif not condition:
#         data = run_query(f"SELECT id, image_url AS image, title, price \
#                             FROM product WHERE title='{product_name}' \
#                             AND categories_id='{category}' AND price <= {price} \
#                             ORDER BY price {sort} LIMIT {page_size}")
#     elif not product_name:
#         data = run_query(f"SELECT id, image_url AS image, title, price \
#                             FROM product WHERE categories_id='{category}' \
#                             AND condition='{condition}' AND price <= {price} \
#                             ORDER BY price {sort} LIMIT {page_size}")
#     elif not category:
#         data = run_query(f"SELECT id, image_url AS image, title, price \
#                             FROM product WHERE title='{product_name}' \
#                             AND condition='{condition}' AND price <= {price} \
#                             ORDER BY price {sort} LIMIT {page_size}")
#     else:
#         data = run_query(f"SELECT id, image_url AS image, title, price \
#                             FROM product WHERE title='{product_name}' AND categories_id='{category}' \
#                             AND condition='{condition}' AND price <= {price} \
#                             ORDER BY price {sort} LIMIT {page_size}")
#     if len(data) < 1:
#         return {"error": "Product not found"}, 400
#     else:
#         data = [{
#             "id": d["id"],
#             "image": join('/image/',d['image']),
#             "title": d["title"],
#             "price": d["price"]
#         }for d in data]
#         return {"data": data, "total_rows" : len(data)}, 200


@product_bp.route("/<path:id>", methods=["GET"])
def getproducts_detail(id): #Done
    data = run_query(f"SELECT p.id, p.brand_name, p.size, p.product_detail, p.price, p.image_url, \
        p.categories_id AS category_id, c.title AS category_name FROM product p \
        RIGHT JOIN categories c ON p.categories_id = c.id \
        WHERE p.id = '{id}' ")
    if len(data) < 1:
        return {"error": "Product not found"}, 400
    else:
        return { "data": data, "message": "Get product detail success" }, 200
    
# @product_bp.route("/search_image", methods=["POST"])
# def search_product():  #TUNGGU TIM AI
#     # product = Table("product", MetaData(bind=get_engine()), autoload=True)
#     # token = str(request.headers.get('token'))
#     # jwt_verification(token)
#     checker = run_query(f"SELECT * FROM users WHERE token='{token}' and admin=True")
#     if not checker:
#         return {"error": "Unauthorized User"}, 401    
#     body = request.json
#     images = body["image"]
    
#     data = run_query(f"SELECT categories_id \
#         FROM product \
#         WHERE image_url = '{images}'")
#     if len(data) < 1:
#         return{"error": "Images not found"}, 400
#     else:
#         return {"data": data, "message":"Search product success"}, 200
    


@product_bp.route("", methods=["GET"])
def getproduct_list(): #ADMIN AND USER
    token = str(request.headers.get('token')) 
    
    param = request.args
    params = param.get
    page = params("page", type=int)
    page_size = params("page_size", type=int)
    sort_by = params("sort_by", type=str)
    category = params("category", type=int)
    price = params("price", type=int)
    condition = params("condition", type=str)
    product_name = params("product_name", type=str)
    
    if sort_by == "price_a_z":
        sort = "ASC"
    elif sort_by == "price_z_a":
        sort = "DESC"
    else:
        return {"error":"sort_by must be price_a_z or price_z_a!"}, 400

    data = run_query(f"SELECT id, image_url AS image, brand_name, price \
                FROM product WHERE brand_name = '{product_name}' AND categories_id ='{category}' \
                AND condition = '{condition}' AND price <= '{price}' AND soft_delete = False \
                ORDER BY price {sort} LIMIT {page_size}")

    if len(data) < 1:
        return {"error": "Product not found"}, 400
    else:
        return {"data": data, "total_rows" : len(data), "message": "Get product list success" }, 200