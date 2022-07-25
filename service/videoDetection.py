# import the opencv module
import cv2
from datetime import datetime
from face_recognition import load_image_file, face_encodings
import glob
from faceComparisonUtil import extract_face, extract_unknown_face_encodings, compare_faces_with_encodings
import os
# Initializing things
from detection.tensorflow.tf_coco_ssd_algorithm import tensor_coco_ssd_mobilenet
from detection.tensorflow.tf_lite_algorithm import perform_object_detection
import customLogging
import requests
import sys

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

logger = customLogging.get_logger("VideoDetection")


def load_criminal_images():
    start_date_time = datetime.now()
    for eachWantedCriminalPath in glob.glob(WANTED_CRIMINALS_PATH):
        criminal_image = load_image_file(eachWantedCriminalPath)
        try:
            criminal_image_encoding = face_encodings(criminal_image)[0]
            criminal_cache.append(criminal_image_encoding)
        except IndexError as e:
            logger.error("An exception occurred while reading {0}".format(eachWantedCriminalPath))
    # Once the loading is done then print
    logger.info(
        "Loaded criminal  {0} images in {1} seconds".format(len(criminal_cache), (datetime.now() - start_date_time)))


def load_known_images():
    start_date_time = datetime.now()
    for eachWantedKnownPersonPath in glob.glob(FAMILIAR_FACES_PATH):
        known_person_image = load_image_file(eachWantedKnownPersonPath)
        try:
            known_person_image_encoding = face_encodings(known_person_image)[0]
            known_person_cache.append(known_person_image_encoding)
        except IndexError as e:
            logger.error("An exception occurred while reading {0}".format(eachWantedKnownPersonPath))
    # Once the loading is done then print
    logger.info(
        "Loaded known  {0} images in {1} seconds".format(len(known_person_cache), (datetime.now() - start_date_time)))


def extract_blur(image, file_name):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    logger.debug(
        "blur ratio {0} for {1}".format(fm, file_name))


def analyze_face(image, count_index):
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
                    analyze_face(image, frame_count)
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


def archive_file(each_video_url):
    logger.info("Archiving {0}".format(each_video_url))
    file_name = os.path.basename(each_video_url)
    os.rename(each_video_url, ARCHIVE_URL + file_name)


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

# start()
