import customLogging
from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
from videoDetection import load_criminal_images, load_known_images, main_method

app = Flask(__name__)
logger = customLogging.get_logger("WebController")


@app.route("/")
def index():
    return "<h1>Welcome to Intelligent detection service!</h1>"


@app.route("/trigger-analysis", methods=['POST'])
def analyze_video():
    video_file = request.form.get('file')
    logger.info("Start: video file name {0}".format(video_file))
    main_method(video_file)
    logger.info("End: video file name {0}".format(video_file))
    return jsonify("success")


if __name__ == '__main__':
    load_criminal_images()
    logger.info("Loaded criminal images")
    load_known_images()
    logger.info("Loaded known images")

    # serve(app, host="0.0.0.0", port=5000, threaded=True)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
