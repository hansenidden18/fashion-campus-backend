from flask import Flask
from cart import cart_bp
from admin import admin_bp
from authentication import auth_bp
from home import home_bp
from product import product_bp
from profile import profile_bp
from categories import categories_bp
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists


def create_app():
    app = Flask(__name__)

    # always register your blueprint(s) when creating application
    blueprints = [cart_bp, admin_bp, auth_bp, home_bp, product_bp, profile_bp, categories_bp]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://posgres:user@postgres:5432/python_docker"
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    if not database_exists(db_url):
        create_database(db_url)
    
    from models.base import db

    db.init_app(app)  # initialize Flask SQLALchemy with this flask app
    Migrate(app, db)

    return app