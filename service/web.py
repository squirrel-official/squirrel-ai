from flask import Flask, request, jsonify

from videoDetection import load_criminal_images, load_known_images, set_config_level

load_criminal_images()
load_known_images()
set_config_level()
app = Flask(__name__)


@app.get("/countries")
def get_countries():
    return jsonify("hello")
