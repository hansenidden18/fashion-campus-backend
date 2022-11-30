from flask import Blueprint, request
from utils import get_engine, jwt_verification, run_query
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

# @product_bp.route("", methods=["POST"])
# def create_product(): #ADMIN
#     product = Table("product", MetaData(bind=get_engine()), autoload=True)

#     token = str(request.headers.get('Authentication'))
#     verif = jwt_verification(token)
#     if "message" in verif:
#         return {"error": "User token expired, please re-login"}, 403
#     body = request.json 
#     product_name = body["product_name"]
#     description = body["description"]
#     images = body["image_url"]
#     condition = body["condition"]
#     category = body["categories_id"]
#     price = body["price"]
    
#     run_query(insert(product).values({f"brand_name":product_name, "product_detail":description, "image_url":images, \
#         "condition":condition, "categories_id":category, "price":price}), commit=True)
#     return {"message": "Product added"}, 200

# @product_bp.route("", methods=["PUT"])
# def update_product(): #ADMIN
#     token = str(request.headers.get('token'))
#     verif = jwt_verification(token)
#     if "message" in verif:
#         return {"error": "User token expired, please re-login"}, 403
    
#     body=request.json
#     product_name = body["product_name"]
#     description = body["description"]
#     images = body["image_url"]
#     condition = body["condition"]
#     category = body["categories_id"]
#     price = body["price"]
#     product_id = body["product_id"]
    
#     data = run_query(f"SELECT from product WHERE id={product_id}")
#     if len(data) < 1:
#         return {"error": "Product id not found"}, 401
#     else:
#         run_query(f"UPDATE product SET brand_name = '{product_name}', product_detail = '{description}', image_url='{images}',\
#             condition = '{condition}', categories_id = '{category}', price = '{price}', id = '{product_id}' WHERE id='{product_id}'", commit=True)
#         return{"message" : "Product updated"}, 200


# @product_bp.route("/<id>", methods=["DELETE"])
# def soft_delete_product(id): #ADMIN
#     token = str(request.headers.get('token'))
#     verif = jwt_verification(token)
#     if "message" in verif:
#         return {"error": "User token expired, please re-login"}, 403
    
#     data = run_query(f"SELECT from product WHERE id={id}")
#     if len(data) < 1:
#         return {"error": "Product id not found"}, 401
#     else:
#         run_query(f"UPDATE product SET soft_delete=True \
#         WHERE id={id}", commit=True)
#         return {"message": "Product deleted"}, 200
    
    

@product_bp.route("/products", methods=["GET"])
def getproduct_list():
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
    if not page_size:
        page_size = 100
    if not condition and not product_name and not category:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE price <= {price} \
                            ORDER BY price {sort} LIMIT {page_size}")
    elif not condition and not category:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE categories_id='{category}' \
                            AND title='{product_name}' AND price <= {price} \
                            ORDER BY price {sort} LIMIT {page_size}")
    elif not product_name and not category:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE categories_id='{category}' \
                            AND condition='{condition}' AND price <= {price} \
                            ORDER BY price {sort} LIMIT {page_size}")
    elif not product_name and not condition:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE categories_id='{category}' \
                            AND price <= {price} \
                            ORDER BY price {sort} LIMIT {page_size}")
    elif not condition:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE title='{product_name}' \
                            AND categories_id='{category}' AND price <= {price} \
                            ORDER BY price {sort} LIMIT {page_size}")
    elif not product_name:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE categories_id='{category}' \
                            AND condition='{condition}' AND price <= {price} \
                            ORDER BY price {sort} LIMIT {page_size}")
    elif not category:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE title='{product_name}' \
                            AND condition='{condition}' AND price <= {price} \
                            ORDER BY price {sort} LIMIT {page_size}")
    else:
        data = run_query(f"SELECT id, image_url AS image, title, price \
                            FROM product WHERE title='{product_name}' AND categories_id='{category}' \
                            AND condition='{condition}' AND price <= {price} \
                            ORDER BY price {sort} LIMIT {page_size}")
    if len(data) < 1:
        return {"error": "Product not found"}, 400
    else:
        data = [{
            "id": d["id"],
            "image": join('/image/',d['image']),
            "title": d["title"],
            "price": d["price"]
        }for d in data]
        return {"data": data, "total_rows" : len(data)}, 200

@product_bp.route("/products/<int:id>", methods=["GET"])
def getproducts_detail(id):
    print(id)
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
            "image_url": join('/image/', d["image_url"]),
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
    
    

# @product_bp.route("/iseng", methods=["GET"])
# def getproductss(): # Ini iseng doang buat ngeliat hasil create 
#     data = run_query(f"SELECT id, brand_name, product_detail, image_url, condition, categories_id, price, soft_delete  FROM product")
#     if len(data) < 1:
#         return {"error": "Product not found"}, 400
#     else:
#         return { "data:": data }, 200
    
# @product_bp.route("/hard/<path:id>", methods=["DELETE"])
# def hard_delete_product(id): #ISENG
#     data = run_query(f"SELECT from product WHERE id={id}")
#     if len(data) < 1:
#         return {"error": "Product id not found"}, 401
#     else:
#         run_query(f"DELETE FROM product WHERE id={id}", commit=True)
#         return {"message": "Product deleted"}, 200
    
    




    
    
    
    
    
    
    
    
    