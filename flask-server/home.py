from flask import Blueprint, request
from utils import run_query

home_bp = Blueprint("home", __name__, url_prefix="")

# BANNER
@home_bp.route("/home/banner", methods=["GET"])
def get_banner():
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


#CATEGORY
@home_bp.route("/home/category", methods=["GET"])
def get_category():
    token = str(request.headers.get('token'))
    if "message" in token:
        return {"error": "User token expired, please re-login"}, 403

    data = run_query (f"SELECT product.id, product.image_url FROM product JOIN categories ON categories.id=product.categories_id GROUP BY categories.title, product.id ORDER BY categories.title")
    if data:
        data = {"data":[{
                "id":d["id"],
                "image":d["image_url"],
                "title":d["title"]} for d in data]}
    else:
        data = []

    return data,200

