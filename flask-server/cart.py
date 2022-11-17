from flask import Blueprint, request

cart_bp = Blueprint("cart", __name__, url_prefix="")

@cart_bp.route("/cart", methods=["GET"])
def get_cart():

    token = str(request.headers.get('token'))