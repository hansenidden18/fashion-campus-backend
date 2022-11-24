from flask import Blueprint, request
from utils import run_query

home_bp = Blueprint("home", __name__, url_prefix="")

# Contoh
@home_bp.route("/home/banner", methods=["GET"])
def add_home():
    token = str(request.headers.get('token'))
    if "message" in token:
        return {"error": "User token expired, please re-login"}, 403

    data = run_query(f"SELECT id, image_url, title FROM product")
    if data:
        data = {"data":[{
                "id":d["id"],
                "image":d["image_url"],
                "title":d["title"]} for d in data]}
    else:
        data = []

    return data,200



@home_bp.route("/home/categories", methods=["GET"])
def add_categories():
    token = str(request.headers.get('token'))
    if "message" in token:
        return {"error": "User token expired, please re-login"}, 403
        
    data = run_query(f"SELECT product.id, product.image FROM product JOIN categories on id GROUP BY categories.title")
    if data:
        data = {"data":[{
                "id":d["id"],
                "image":d["image_url"],
                "category_name":d["title"]} for d in data]}
    else:
        data = []

    return data,200


