import flask
from flask import render_template, request

from faceComparisonUtil import compare_faces

app = flask.Flask(__name__)


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    return render_template("index.html")


@app.route('/upload-success', methods=['POST'])
def home():
    file = request.files['myfile']
    known_image = "/Users/anil/Desktop/known_image.png"
    unknown_image_path = "/Users/anil/Desktop/unknown.jpeg"
    compare_faces(known_image, unknown_image_path)
    return "done"
