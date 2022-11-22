from flask import url_for, redirect
from utils import allowed_file
from models.models import create_app

app = create_app()

@app.route("/")
def get_hello():
    return "selamat datang!!!"

@app.route("/image/<filename>")
def get_image(filename):
    if allowed_file(filename):
        return url_for('static', filename='uploads/' + filename)
    else:
        return {"message":'Allowed image types are -> png, jpg, jpeg, gif'}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')