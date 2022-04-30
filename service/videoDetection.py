# import the opencv module
import cv2
from datetime import datetime
import logging
from face_recognition import load_image_file, face_encodings
import glob
from faceComparisonUtil import extract_face, extract_unknown_face_encodings, compare_faces_with_encodings
import os

# Initializing things
from detection.tensorflow.tf_coco_ssd_algorithm import tensor_coco_ssd_mobilenet
from detection.tensorflow.tf_lite_algorithm import perform_object_detection

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
for eachWantedCriminalPath in glob.glob('/usr/local/squirrel-ai/wanted-criminals/*'):
    criminal_image = load_image_file(eachWantedCriminalPath)
    criminal_image_encoding = face_encodings(criminal_image)[0]
    criminal_cache.append(criminal_image_encoding)
endDateTime = datetime.now()
# Once the loading is done then print
logging.info("Loaded criminal  {0} images in {1} seconds".format(len(criminal_cache), (endDateTime - startDateTime)))

startDateTime = datetime.now()
for eachWantedKnownPersonPath in glob.glob('/usr/local/squirrel-ai/known/*'):
    known_person_image = load_image_file(eachWantedKnownPersonPath)
    known_person_image_encoding = face_encodings(known_person_image)[0]
    known_person_cache.append(known_person_image_encoding)
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
                cv2.imwrite('/usr/local/squirrel-ai/captured/frame{:d}.jpg'.format(count_index), unknown_face_image)

        for each_known_encoding in known_person_cache:
            if compare_faces_with_encodings(each_known_encoding, unknown_face_image_encodings,
                                            "eachWantedKnownPath"):
                cv2.imwrite('/usr/local/squirrel-ai/captured/known-frame{:d}.jpg'.format(count_index),
                            unknown_face_image)

        end_date_time = datetime.now()
        logging.debug("Total comparison time is {0} seconds".format((end_date_time - start_date_time)))
        count_index += 1


def main_method(videoUrl):
    # setting the camera resolution and frame per second 1296 972
    capture = cv2.VideoCapture(videoUrl)
    if not capture.isOpened():
        logging.error("Error opening video file")
    global x, y

    while capture.isOpened():
        # to read frame by frame
        _, image = capture.read()
        if tensor_coco_ssd_mobilenet(image, ssd_model_path, logging) \
                and perform_object_detection(image, efficientdet_lite0_path, bool(0), logging):
            # cv2.rectangle(image_2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            process_face(image, count)
            cv2.imwrite('/usr/local/squirrel-ai/visitor/' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.jpg',
                        image)


try:
    for eachVideoUrl in glob.glob('/var/lib/motion/*'):
        main_method(eachVideoUrl)
        # os.rename(eachVideoUrl, "path/to/new/destination/for/file.foo")
except Exception as e:
    logging.error("Oops!", e.__class__, "occurred.")
