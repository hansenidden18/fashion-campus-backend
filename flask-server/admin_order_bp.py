from flask import Blueprint, request
from utils import run_query, get_engine, jwt_verification, admin_token_checker
from sqlalchemy import insert, Table, MetaData

admin_order_bp = Blueprint("admin_order", __name__, url_prefix="/order")