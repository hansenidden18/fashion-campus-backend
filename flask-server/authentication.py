from flask import Blueprint, request
from utils import run_query

auth_bp = Blueprint("authentication", __name__, url_prefix="")

@auth_bp.route("/sign-up", methods=["POST"])
def add_user():
    body = request.json

    name = body['name']
    email = body['email']
    phone_number = body['phone_number']
    password = body['password']