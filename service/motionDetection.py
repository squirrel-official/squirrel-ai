import cv2
from customLogging.customLogging import get_logger
# Initializing things
from detection.tensorflow.tf_coco_ssd_algorithm import tensor_coco_ssd_mobilenet
from detection.tensorflow.tf_lite_algorithm import perform_object_detection
from faceService import analyze_face
from imageLoadService import load_criminal_images, load_known_images
from memory_profiler import profile
import random

# For writing
UNKNOWN_VISITORS_PATH = '/usr/local/squirrel-ai/result/unknown-visitors/'

CAMERA_STREAM = '/dev/video0'
NOTIFICATION_URL = 'http://ai-security.local:8087/visitor'
count = 0
ssd_model_path = '/usr/local/squirrel-ai/model/coco-ssd-mobilenet'
efficientdet_lite0_path = '/usr/local/squirrel-ai/model/efficientdet-lite0/efficientdet_lite0.tflite'
logger = get_logger("Motion Detection")


@profile
def monitor_camera_stream(streamUrl, criminal_cache, known_person_cache):
    try:
        cv2.setUseOptimized(True)
        capture = cv2.VideoCapture(streamUrl, cv2.CAP_V4L2)
        # 2048 * 1536 , 2592 * 1944 , 2272 * 1704,
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 2048)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1536)
        if not capture.isOpened():
            logger.error("Error opening video file {0}".format(streamUrl))

        frame_count = 1
        if capture.isOpened():
            ret, image = capture.read()
            logger.info("Processing file {0} ".format(streamUrl))
            logger.info("Frame rate: {0} ".format(capture.get(cv2.CAP_PROP_FPS)))
            while ret:
                # cv2.imwrite('{}All-frame{:d}.jpg'.format('/usr/local/squirrel-ai/result/captured-criminals/', random.randint(0, 1000)), image)
                if perform_object_detection(image, efficientdet_lite0_path, bool(0)):
                    logger.debug("Object detected")
                    analyze_face(image, frame_count, criminal_cache, known_person_cache)
                ret, image = capture.read()
    except Exception as e:
        logger.error("An exception occurred.")
        logger.error(e, exc_info=True)


def start_monitoring():
    try:
        criminal_cache = load_criminal_images()
        known_person_cache = load_known_images()
        monitor_camera_stream(CAMERA_STREAM, criminal_cache, known_person_cache)
    except Exception as e:
        logger.error("An exception occurred.")
        logger.error(e, exc_info=True)


start_monitoring()
