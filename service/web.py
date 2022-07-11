import logging

from flask import Flask, request, jsonify
from waitress import serve

from videoDetection import load_criminal_images, load_known_images, set_config_level, MOTION_VIDEO_URL, main_method

load_criminal_images()
load_known_images()
set_config_level()
app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Welcome to Intelligent detection service!</h1>"


@app.get("/trigger-analysis")
def get_countries():
    video_file_name = request.args.get('file')
    logging.info("Video file name {0}".format(video_file_name))
    complete_video_path = MOTION_VIDEO_URL + video_file_name
    main_method(complete_video_path)
    return jsonify("success")


serve(app, port=9999)
