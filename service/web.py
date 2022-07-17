import logging

from flask import Flask, request, jsonify
from waitress import serve
import configparser

from videoDetection import load_criminal_images, load_known_images, set_config_level, main_method, CONFIG_PROPERTIES

logging.basicConfig(filename='/usr/local/squirrel-ai/logs/service.log',
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %('
                               'funcName)s: %(message)s', level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S')
config = configparser.ConfigParser()
config.read(CONFIG_PROPERTIES)
log_level = config['DEFAULT']['log.level']
logging.info("changing log level to {0}".format(log_level))
if log_level == 'DEBUG':
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.ERROR)

load_criminal_images()
load_known_images()
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
