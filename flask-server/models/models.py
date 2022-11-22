from flask import Flask
from cart import cart_bp
from admin import admin_bp
from authentication import auth_bp
from home import home_bp
from product import product_bp
from profile import profile_bp
from flask_migrate import Migrate
from sqlalchemy_utils import create_database, database_exists


def create_app():
    app = Flask(__name__)

    # always register your blueprint(s) when creating application
    blueprints = [cart_bp, admin_bp, auth_bp, home_bp, product_bp, profile_bp]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    
    UPLOAD_FOLDER = 'static/uploads/'

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://posgres:user@postgres:5432/python_docker"
    app.config
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    if not database_exists(db_url):
        create_database(db_url)
    
    from models.base import db

    db.init_app(app)  # initialize Flask SQLALchemy with this flask app
    Migrate(app, db)

    return app