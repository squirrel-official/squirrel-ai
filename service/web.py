import logging

from flask import Flask, request, jsonify
from waitress import serve

from videoDetection import load_criminal_images, load_known_images, set_config_level, main_method

# load_criminal_images()
# load_known_images()
# set_config_level()
app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Welcome to Intelligent detection service!</h1>"


@app.route("/trigger-analysis")
def get_countries():
    motion_video_directory = '/var/lib/motion/'
    video_file_name = request.args.get('file')
    logging.info("Video file name {0}".format(video_file_name))
    complete_video_path = motion_video_directory + video_file_name
    main_method(complete_video_path)
    return jsonify("success")


if __name__ == '__main__':
    load_criminal_images()
    load_known_images()
    set_config_level()
    serve(app, host="0.0.0.0", port=5000)
