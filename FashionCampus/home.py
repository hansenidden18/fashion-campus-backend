from flask import Blueprint, request
from utils import run_query
from os.path import join, dirname, realpath

home_bp = Blueprint("home", __name__, url_prefix="")

# BANNER
@home_bp.route("/home/banner", methods=["GET"])
def get_banner():
    data = run_query(f"SELECT id, image_url, title FROM banner")
    if data:
        data = {"data":[{
                "id":d["id"],
                "image":join("/image/",d["image_url"]),
                "title":d["title"]} for d in data]}
    else:
        data = []
    # print(send_from_directory(directory=paths,path=data[0]["image_url"]))
    return data,200


#CATEGORY
@home_bp.route("/home/category", methods=["GET"])
def get_category():
    data = run_query (f'''SELECT product.id, product.image_url, categories.title  FROM product 
                            JOIN categories ON categories.id=product.categories_id ORDER BY categories.title ASC LIMIT 4''')
    
    if data:
        data = {"data":[{
                "id":d["id"],
                "image":join('/image/',d["image_url"][0]),
                "title":d["title"]} for d in data]}
    else:
        data = []

    return data,200
