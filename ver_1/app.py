from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
from contours import resistor_value
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return render_template("index.html", result="No image uploaded.")

    file = request.files["image"]
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    result = resistor_value(filepath)
    if "error" in result:
        return render_template("index.html", result=result["error"])
    else:
        return render_template("index.html", result=result["value"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)