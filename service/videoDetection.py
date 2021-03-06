# import the opencv module
import glob
import os

import cv2
from datetime import datetime

# Initializing things
from detection.tensorflow.tf_coco_ssd_algorithm import tensor_coco_ssd_mobilenet
from detection.tensorflow.tf_lite_algorithm import perform_object_detection
from service.faceService import analyze_face
from service.fileService import archive_file
from service.imageLoadService import load_criminal_images, load_known_images
from customLogging.customLogging import get_logger
import requests

VISITOR_NOTIFICATION_URL = 'http://my-security.local:8087/visitor'

MOTION_VIDEO_URL = '/var/lib/motion/*'

# For writing
UNKNOWN_VISITORS_PATH = '/usr/local/squirrel-ai/result/unknown-visitors/'

ssd_model_path = '/usr/local/squirrel-ai/model/coco-ssd-mobilenet'
efficientdet_lite0_path = '/usr/local/squirrel-ai/model/efficientdet-lite0/efficientdet_lite0.tflite'

logger = get_logger("VideoDetection")

criminal_cache = []
known_person_cache = []


def analyze_each_video(videoUrl):
    start_index = videoUrl.rindex("/") + 1
    camera_id = videoUrl[start_index: start_index + 1]
    capture = cv2.VideoCapture(videoUrl)
    stat_info = os.stat(videoUrl)
    size = stat_info.st_size
    if not capture.isOpened():
        logger.error("Error opening video file {}".format(videoUrl))

    frame_count = 0
    file_processed = 0
    image_number = 1
    if capture.isOpened():
        ret, image = capture.read()
        video_length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if video_length > 0:
            logger.info(" Processing file {0} and  number of frames:{1}".format(videoUrl, video_length))
            while ret:
                file_processed = 1
                if tensor_coco_ssd_mobilenet(image, ssd_model_path) \
                        and perform_object_detection(image, efficientdet_lite0_path, bool(0)):
                    logger.debug("passed object detection".format(video_length))
                    analyze_face(image, frame_count, criminal_cache, known_person_cache)
                    complete_file_name = UNKNOWN_VISITORS_PATH + str(camera_id) + "-" + str(
                        image_number) + "-" + datetime.now().strftime("%Y%m%d%H%M") + '.jpg'
                    cv2.imwrite(complete_file_name, image)
                    # extract_blur(image, complete_file_name)
                    image_number += 1
                ret, image = capture.read()
        else:
            file_processed = 0
            logger.debug(
                "file {0} and  number of frames:{1} and size {2} not processed".format(videoUrl, video_length,
                                                                                       size))
    else:
        capture.release()
        # file_processed = 1
        logger.debug("Not processed seems to be some issue with file {0} with size {1}".format(videoUrl, size))
    # Archive the file since it has been processed
    if bool(file_processed):
        requests.post(VISITOR_NOTIFICATION_URL)
        archive_file(videoUrl)


def detect_from_videos():
    try:
        load_criminal_images()
        load_known_images()
        while True:
            for eachVideoUrl in glob.glob(MOTION_VIDEO_URL):
                analyze_each_video(eachVideoUrl)

    except Exception as e:
        logger.error("An exception occurred.")
        logger.error(e, exc_info=True)

# detect_from_videos()
