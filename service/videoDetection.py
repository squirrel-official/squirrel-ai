# import the opencv module
import configparser
import cv2
from datetime import datetime
from face_recognition import load_image_file, face_encodings
import glob
from faceComparisonUtil import extract_face, extract_unknown_face_encodings, compare_faces_with_encodings
import os
# Initializing things
from detection.tensorflow.tf_coco_ssd_algorithm import tensor_coco_ssd_mobilenet
from detection.tensorflow.tf_lite_algorithm import perform_object_detection
import logging

EXECUTION_DELAY = 10

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

logging.basicConfig(filename='/usr/local/squirrel-ai/logs/service.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %('
                           'funcName)s: %(message)s', level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

ssd_model_path = '/usr/local/squirrel-ai/model/coco-ssd-mobilenet'
efficientdet_lite0_path = '/usr/local/squirrel-ai/model/efficientdet-lite0/efficientdet_lite0.tflite'

startDateTime = datetime.now()
for eachWantedCriminalPath in glob.glob(WANTED_CRIMINALS_PATH):
    criminal_image = load_image_file(eachWantedCriminalPath)
    try:
        criminal_image_encoding = face_encodings(criminal_image)[0]
        criminal_cache.append(criminal_image_encoding)
    except IndexError as e:
        logging.error("An exception occurred while reading {0}".format(eachWantedCriminalPath))

endDateTime = datetime.now()
# Once the loading is done then print
logging.info("Loaded criminal  {0} images in {1} seconds".format(len(criminal_cache), (endDateTime - startDateTime)))

startDateTime = datetime.now()
for eachWantedKnownPersonPath in glob.glob(FAMILIAR_FACES_PATH):
    known_person_image = load_image_file(eachWantedKnownPersonPath)
    try:
        known_person_image_encoding = face_encodings(known_person_image)[0]
        known_person_cache.append(known_person_image_encoding)
    except IndexError as e:
        logging.error("An exception occurred while reading {0}".format(eachWantedKnownPersonPath))
endDateTime = datetime.now()
# Once the loading is done then print
logging.info("Loaded known  {0} images in {1} seconds".format(len(known_person_cache), (endDateTime - startDateTime)))


def process_face(image, count_index):
    unknown_face_image = extract_face(image)
    if unknown_face_image is not None:
        logging.debug('A new person identified by face so processing it')
        unknown_face_image_encodings = extract_unknown_face_encodings(unknown_face_image)
        # saving the image to visitor folder
        start_date_time = datetime.now()
        for each_criminal_encoding in criminal_cache:
            if compare_faces_with_encodings(each_criminal_encoding, unknown_face_image_encodings,
                                            "eachWantedCriminalPath"):
                cv2.imwrite('{}criminal-frame{:d}.jpg'.format(CAPTURED_CRIMINALS_PATH, count_index),
                            unknown_face_image)

        for each_known_encoding in known_person_cache:
            if compare_faces_with_encodings(each_known_encoding, unknown_face_image_encodings,
                                            "eachWantedKnownPath"):
                cv2.imwrite('{}known-frame{:d}.jpg'.format(KNOWN_VISITORS_PATH, count_index),
                            unknown_face_image)
        end_date_time = datetime.now()

        cv2.imwrite('/usr/local/squirrel-ai/result/unknown-visitors/face-frame{:d}.jpg'.format(count_index),
                    unknown_face_image)
        logging.debug("Total comparison time is {0} seconds".format((end_date_time - start_date_time)))
        count_index += 1


def main_method(videoUrl):
    capture = cv2.VideoCapture(videoUrl)
    if not capture.isOpened():
        logging.error("Error opening video file {}".format(videoUrl))
    global x, y

    frame_count = 0
    file_processed = 0
    if capture.isOpened():
        ret, image = capture.read()
        video_length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        logging.debug("Number of frames:{0} ".format(video_length))
        if video_length > 0:
            while ret:
                file_processed = 1
                if tensor_coco_ssd_mobilenet(image, ssd_model_path, logging) \
                        and perform_object_detection(image, efficientdet_lite0_path, bool(0), logging):
                    logging.debug("passed object detection".format(video_length))
                    process_face(image, frame_count)
                    cv2.imwrite(UNKNOWN_VISITORS_PATH + datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg',
                                image)
                ret, image = capture.read()
        else:
            file_processed = 0
    else:
        capture.release()
        file_processed = 1
        logging.error("Archiving the file, seems to be some issue with file. released {0}".format(videoUrl))
    # Archive the file since it has been processed
    if bool(file_processed):
        archive_file(videoUrl)


def archive_file(each_video_url):
    logging.info("Archiving {0}".format(each_video_url))
    file_name = os.path.basename(each_video_url)
    os.rename(each_video_url, ARCHIVE_URL + file_name)


def set_config_level():
    config = configparser.ConfigParser()
    config.read(CONFIG_PROPERTIES)
    log_level = config['DEFAULT']['log.level']
    logging.info("changing log level to {0}".format(log_level))
    if log_level == 'DEBUG':
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.ERROR)


set_config_level()
DATE_TIME_FORMAT = "%Y%m%d%H%M%S"
try:
    while True:
        currentDateTime = datetime.strptime(datetime.today().strftime(DATE_TIME_FORMAT), DATE_TIME_FORMAT)
        for eachVideoUrl in glob.glob(MOTION_VIDEO_URL):
            stat_info = os.stat(eachVideoUrl)
            size = stat_info.st_size

            date_time = eachVideoUrl[-18: -4]
            dateTimeFromFileName = datetime.strptime(date_time, DATE_TIME_FORMAT)
            if (currentDateTime - dateTimeFromFileName).seconds > EXECUTION_DELAY:
                logging.info(" Processing file {} of size {} mb with extracted time as {}".format(eachVideoUrl, size / (1024 * 1024), dateTimeFromFileName))
                main_method(eachVideoUrl)
            else:
                logging.debug("Not processing-date time difference for file {} is {} ".format(eachVideoUrl,
                                                                                             (currentDateTime - dateTimeFromFileName).seconds))
except Exception as e:
    logging.error("An exception : ", e, "occurred.")
