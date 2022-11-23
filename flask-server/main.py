from flask import url_for, redirect
from utils import allowed_file
from models.models import create_app
import io
from os.path import join, dirname, realpath
from base64 import encodebytes
from PIL import Image

app = create_app()

@app.route("/")
def get_hello():
    return "selamat datang!!!"

@app.route("/image/<filename>")
def get_image(filename):
    if allowed_file(filename):
        path = join(dirname(realpath(__file__)), app.config['UPLOAD_FOLDER'])
        pil_image = Image.open(join(path, filename), mode='r')
        byte_arr = io.BytesIO()
        pil_image.save(byte_arr, format='PNG')
        encoded_image = encodebytes(byte_arr.getvalue()).decode('ascii')
        return encoded_image, 200
    else:
        return {"message":'Allowed image types are -> png, jpg, jpeg, gif'}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')