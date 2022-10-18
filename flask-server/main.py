from flask import Flask
from cart import cart_bp
from admin import admin_bp
from authentication import auth_bp
from home import home_bp
from product import product_bp
from profile import profile_bp

def create_app():
    app = Flask(__name__)

    # always register your blueprint(s) when creating application
    blueprints = [cart_bp, admin_bp, auth_bp, home_bp, product_bp, profile_bp]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app

app = create_app()

@app.route("/")
def get_hello():
    return "selamat datang!!!"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')