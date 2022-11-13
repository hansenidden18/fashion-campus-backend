from utils import get_engine, run_query
from flask import Blueprint, request
from sqlalchemy import (
    MetaData,
    Table,
    delete,
    insert,
    select,
)
from sqlalchemy.exc import IntegrityError

home_bp = Blueprint("home", __name__, url_prefix="/home/banner")

# Contoh
@home_bp.route("", methods=["POST"])
def add_home():
    body = request.json
    id = body["id"]
    image = body["image"]
    title = body["title"]

    home = Table("home", MetaData(bind=get_engine()), autoload=True)
    try:
        run_query(insert(home).values({"id": id},{"image": image},{"title": title}), commit=True)
        return {"message": f"Home {id}{image}{title} is added"}, 201
    except IntegrityError:
        # case: when the home already exists
        return {"error": "Home with the same title already exists"}, 400

@home_bp.route("", methods=["DELETE"])
def delete_home():
    body = request.json
    id = body["id"]
    image = body["image"]
    title = body["title"]

    # check information about the book
    home = Table("home", MetaData(bind=get_engine()), autoload=True)
    home_details = run_query(select(home).where(home.c.id == id, image == image, title == title))

    # case; book doesn't exist
    if not home_details:
        return {"error": "Home is not known"}, 400

    # case: book is currently borrowed
    borrower = home_details[0]["borrower"]
    if borrower:
        return {"error": f"Home is currently borrowed by {borrower}"}, 403

    # remove book validly
    run_query(delete(home).where(home.c.id == id, image == image, title == title), commit=True)
    return {"message": f"Home {id}{image}{title} is removed"}




