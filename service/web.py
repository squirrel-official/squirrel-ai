import logging

from flask import Flask, request, jsonify
from waitress import serve

from videoDetection import load_criminal_images, load_known_images, set_config_level, main_method

load_criminal_images()
load_known_images()
set_config_level()
app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Welcome to Intelligent detection service!</h1>"


@app.route("/trigger-analysis", methods=['POST'])
def get_countries():
    video_file = request.form.get('file')
    logging.info("Video file name {0}".format(video_file))
    main_method(video_file)
    return jsonify("success")


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
