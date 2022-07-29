# import the opencv module
import time
import cv2
from customLogging.customLogging import get_logger
# Initializing things
from detection.tensorflow.tf_coco_ssd_algorithm import tensor_coco_ssd_mobilenet
from detection.tensorflow.tf_lite_algorithm import perform_object_detection
from faceService import analyze_face
from imageLoadService import load_criminal_images, load_known_images
import threading
import requests

# For writing
UNKNOWN_VISITORS_PATH = '/usr/local/squirrel-ai/result/unknown-visitors/'

GARAGE_EXTERNAL_CAMERA_STREAM = '/dev/video4'
GATE_EXTERNAL_CAMERA_STREAM = '/dev/video5'
NOTIFICATION_URL = 'http://my-security.local:8087/visitor'
count = 0
ssd_model_path = '/usr/local/squirrel-ai/model/coco-ssd-mobilenet'
efficientdet_lite0_path = '/usr/local/squirrel-ai/model/efficientdet-lite0/efficientdet_lite0.tflite'
logger = get_logger("Motion Detection")


def monitor_camera_stream(streamUrl, camera_id, criminal_cache, known_person_cache):
    capture = cv2.VideoCapture(streamUrl)
    if not capture.isOpened():
        logger.error("Error opening video file {}".format(streamUrl))

    frame_count = 1
    image_count = 1
    object_detection_flag = 0
    if capture.isOpened():
        ret, image = capture.read()
        logger.info(" Processing file {0} ".format(streamUrl))
        while ret:
            if tensor_coco_ssd_mobilenet(image, ssd_model_path) \
                    and perform_object_detection(image, efficientdet_lite0_path, bool(0)):
                logger.debug("Object detected, flag :{0}".format(object_detection_flag))
                if object_detection_flag == 0:
                    detection_counter = time.time()
                    object_detection_flag = 1

                complete_file_name = UNKNOWN_VISITORS_PATH + str(camera_id) + "-" + str(image_count) + '.jpg'
                image_count = image_count + 1
                cv2.imwrite(complete_file_name, image)
                if (time.time() - detection_counter) > 5:
                    object_detection_flag = 0
                    data = requests.post(NOTIFICATION_URL)
                    logger.info("Detected activity sent notification, response : {0}".format(data.reason))

                analyze_face(image, frame_count, criminal_cache, known_person_cache)

            ret, image = capture.read()


def start_monitoring():
    try:
        criminal_cache = load_criminal_images()
        known_person_cache = load_known_images()
        t1 = threading.Thread(target=monitor_camera_stream,
                              args=(GARAGE_EXTERNAL_CAMERA_STREAM, 1, criminal_cache, known_person_cache))
        t2 = threading.Thread(target=monitor_camera_stream,
                              args=(GATE_EXTERNAL_CAMERA_STREAM, 2, criminal_cache, known_person_cache))
        t1.start()
        t2.start()
        # monitor_camera_stream(GARAGE_EXTERNAL_CAMERA_STREAM, 1)
        # monitor_camera_stream(GATE_EXTERNAL_CAMERA_STREAM, 2)

    except Exception as e:
        logger.error("An exception occurred.")
        logger.error(e, exc_info=True)


start_monitoring()
