# import the opencv module
import configparser
import cv2
from datetime import datetime
import glob
from faceComparisonUtil import extract_face, extract_unknown_face_encodings, compare_faces_with_encodings
import os
import customLogging
import requests

CRIMINAL_NOTIFICATION_URL = 'http://my-security.local:8087/criminal'
VISITOR_NOTIFICATION_URL = 'http://my-security.local:8087/visitor'
FRIEND_NOTIFICATION_URL = 'http://my-security.local:8087/friend'

MOTION_VIDEO_URL = '/var/lib/motion/*'
CONFIG_PROPERTIES = '/usr/local/squirrel-ai/config.properties'
ARCHIVE_URL = "/usr/local/squirrel-ai/data/archives/"

# For writing
UNKNOWN_VISITORS_PATH = '/usr/local/squirrel-ai/result/unknown-visitors/'
CAPTURED_CRIMINALS_PATH = '/usr/local/squirrel-ai/result/captured-criminals/'
KNOWN_VISITORS_PATH = '/usr/local/squirrel-ai/result/known-visitors/'

# For reading
FAMILIAR_FACES_PATH = '/usr/local/squirrel-ai/data/familiar-faces/*'
WANTED_CRIMINALS_PATH = '/usr/local/squirrel-ai/data/wanted-criminals/*'

count = 0
criminal_cache = []
known_person_cache = []

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

ssd_model_path = '/usr/local/squirrel-ai/model/coco-ssd-mobilenet'
efficientdet_lite0_path = '/usr/local/squirrel-ai/model/efficientdet-lite0/efficientdet_lite0.tflite'
DATE_TIME_FORMAT = "%Y%m%d%H%M%S"

logger = customLogging.get_logger("VideoDetection")


def process_face(image, count_index):
    unknown_face_image = extract_face(image)
    if unknown_face_image is not None:
        logger.debug('A new person identified by face so processing it')
        unknown_face_image_encodings = extract_unknown_face_encodings(unknown_face_image)
        # saving the image to visitor folder
        start_date_time = datetime.now()
        for each_criminal_encoding in criminal_cache:
            if compare_faces_with_encodings(each_criminal_encoding, unknown_face_image_encodings,
                                            "eachWantedCriminalPath"):
                cv2.imwrite('{}criminal-frame{:d}.jpg'.format(CAPTURED_CRIMINALS_PATH, count_index),
                            unknown_face_image)
                requests.post(CRIMINAL_NOTIFICATION_URL)

        for each_known_encoding in known_person_cache:
            if compare_faces_with_encodings(each_known_encoding, unknown_face_image_encodings,
                                            "eachWantedKnownPath"):
                cv2.imwrite('{}known-frame{:d}.jpg'.format(KNOWN_VISITORS_PATH, count_index),
                            unknown_face_image)
                requests.post(FRIEND_NOTIFICATION_URL)
        end_date_time = datetime.now()
        logger.debug("Total comparison time is {0} seconds".format((end_date_time - start_date_time)))
        count_index += 1


def main_method(videoUrl):
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

                ret, image = capture.read()
        else:
            file_processed = 0
            logger.debug(
                "file {0} and  number of frames:{1} and size {2} not processed".format(videoUrl, video_length,
                                                                                       size))
    else:
        capture.release()
        logger.debug("Not processed seems to be some issue with file {0} with size {1}".format(videoUrl, size))
    # Archive the file since it has been processed
    if bool(file_processed):
        requests.post(VISITOR_NOTIFICATION_URL)


def start():
    try:
        while True:
            for eachVideoUrl in glob.glob(MOTION_VIDEO_URL):
                main_method(eachVideoUrl)

    except Exception as e:
        logger.error("An exception occurred.")
        logger.error(e, exc_info=True)

# start()
