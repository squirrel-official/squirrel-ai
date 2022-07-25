# import the opencv module
import cv2
from datetime import datetime
from customLogging.customLogging import get_logger
import os
# Initializing things
from detection.tensorflow.tf_coco_ssd_algorithm import tensor_coco_ssd_mobilenet
from detection.tensorflow.tf_lite_algorithm import perform_object_detection
from faceService import analyze_face
from imageLoadService import load_criminal_images, load_known_images

import requests

VISITOR_NOTIFICATION_URL = 'http://my-security.local:8087/visitor'
MOTION_VIDEO_URL = '/var/lib/motion/*'

# For writing
UNKNOWN_VISITORS_PATH = '/usr/local/squirrel-ai/result/unknown-visitors/'
NOTIFICATION_URL = 'http://my-security.local:8087/notification?camera-id'

GARAGE_EXTERNAL_CAMERA_STREAM = 'http://my-security.local:7776/1/stream'

count = 0
criminal_cache = []
known_person_cache = []
ssd_model_path = '/usr/local/squirrel-ai/model/coco-ssd-mobilenet'
efficientdet_lite0_path = '/usr/local/squirrel-ai/model/efficientdet-lite0/efficientdet_lite0.tflite'
logger = get_logger("Motion Detection")


def analyze_each_video(videoUrl, camera_id):
    capture = cv2.VideoCapture(videoUrl)
    if not capture.isOpened():
        logger.error("Error opening video file {}".format(videoUrl))

    frame_count = 0
    if capture.isOpened():
        ret, image = capture.read()
        logger.info(" Processing file {0} ".format(videoUrl))
        while ret:
            if tensor_coco_ssd_mobilenet(image, ssd_model_path) \
                    and perform_object_detection(image, efficientdet_lite0_path, bool(0)):
                logger.debug("passed object detection")
                analyze_face(image, frame_count)
                complete_file_name = UNKNOWN_VISITORS_PATH + str(camera_id) + "-" + datetime.now().strftime(
                    "%Y%m%d%H%M") + '.jpg'
                cv2.imwrite(complete_file_name, image)
            ret, image = capture.read()


def start_monitoring():
    try:
        load_criminal_images()
        load_known_images()
        analyze_each_video(GARAGE_EXTERNAL_CAMERA_STREAM, 1)

    except Exception as e:
        logger.error("An exception occurred.")
        logger.error(e, exc_info=True)


start_monitoring()
