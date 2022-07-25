import customLogging
from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
from videoDetection import load_criminal_images, load_known_images, analyze_each_video
import time

app = Flask(__name__)
logger = customLogging.get_logger("WebController")


@app.route("/")
def index():
    return "<h1>Welcome to Intelligent detection service!</h1>"


@app.route("/trigger-analysis", methods=['POST'])
def analyze_video():
    video_file = request.form.get('file')
    start_time = time.time()
    analyze_each_video(video_file)
    logger.info("End: processed video file name {0} in {1} seconds".format(video_file, round(time.time() - start_time)))
    return jsonify("success")


if __name__ == '__main__':
    load_criminal_images()
    load_known_images()
    # serve(app, host="0.0.0.0", port=5000, threaded=True)
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
