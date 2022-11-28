from models.models import create_app

app = create_app()

@app.route("/")
def get_hello():
    return "selamat datang!!!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')