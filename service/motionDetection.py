# import the opencv module
import cv2
from datetime import datetime
import logging
from face_recognition import load_image_file, face_encodings
from service.detection.opencv.detection_util import is_human_present, is_car_present
import glob
from faceComparisonUtil import extract_face, extract_unknown_face_encodings, compare_faces_with_encodings

# Initializing things
count = 0
criminal_cache = []
logging.basicConfig(filename='../logs/service.log', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# setting the camera resolution and frame per second 1296 972
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
capture.set(cv2.CAP_PROP_FPS, 10)

startDateTime = datetime.now()
for eachWantedCriminalPath in glob.glob('/usr/local/squirrel-ai/wanted-criminals/*'):
    criminal_image = load_image_file(eachWantedCriminalPath)
    criminal_image_encoding = face_encodings(criminal_image)[0]
    criminal_cache.append(criminal_image_encoding)
endDateTime = datetime.now()
# Once the loading is done then print
logging.info("Loaded {0} images in {1} seconds".format(len(criminal_cache), (endDateTime - startDateTime)))

if not capture.isOpened():
    logging.error("Error opening video stream or file")


def process_face(image, count_index):
    unknown_face_image = extract_face(image)
    if unknown_face_image is not None:
        logging.debug('A new person identified by face so processing it')
        unknown_face_image_encodings = extract_unknown_face_encodings(unknown_face_image)
        # saving the image to visitor folder
        start_date_time = datetime.now()
        start_timestamp_str = start_date_time.strftime("%Y%m%d-%H%M%S")
        cv2.imwrite('/usr/local/squirrel-ai/visitor/' + start_timestamp_str + '.jpg', image)
        for each_criminal_encoding in criminal_cache:
            if compare_faces_with_encodings(each_criminal_encoding, unknown_face_image_encodings,
                                            "eachWantedCriminalPath"):
                cv2.imwrite('/usr/local/squirrel-ai/captured/frame{:d}.jpg'.format(count_index), unknown_face_image)
        end_date_time = datetime.now()
        logging.debug("Total comparison time is {0} seconds".format((end_date_time - start_date_time)))
        count_index += 1


while capture.isOpened():
    # to read frame by frame
    _, image_1 = capture.read()
    _, image_2 = capture.read()
    # find difference between two frames
    diff = cv2.absdiff(image_1, image_2)

    # to convert the frame to grayscale
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # apply some blur to smoothen the frame
    diff_blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)

    # to get the binary image
    _, thresh_bin = cv2.threshold(diff_blur, 20, 255, cv2.THRESH_BINARY)

    # to find contours
    contours, hierarchy = cv2.findContours(thresh_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # to draw the bounding box when the motion is detected
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 500 and (is_human_present(hog, image_2) or is_car_present(image_2)):
            cv2.rectangle(image_2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            process_face(image_2, count)
            cv2.imwrite('/usr/local/squirrel-ai/captured/motion{:d}.jpg'.format(count), image_1)
    # cv2.drawContours(img_1, contours, -1, (0, 255, 0), 2)

    # display the output
    # cv2.imwrite('/usr/local/squirrel-ai/captured/motion{:d}.jpg'.format(count), img_1)
    if cv2.waitKey(100) == 13:
        exit()
