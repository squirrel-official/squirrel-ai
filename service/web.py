import logging

from flask import Flask, request, jsonify
from waitress import serve
import configparser

from videoDetection import load_criminal_images, load_known_images, set_config_level, main_method, CONFIG_PROPERTIES


def load_logging_level():
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


load_logging_level()
load_criminal_images()
load_known_images()
logger = logging.getLogger("WebController")
app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Welcome to Intelligent detection service!</h1>"


@app.route("/trigger-analysis", methods=['POST'])
def analyze_video():
    video_file = request.form.get('file')
    logger.info("Video file name {0}".format(video_file))
    main_method(video_file, logger)
    return jsonify("success")


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
