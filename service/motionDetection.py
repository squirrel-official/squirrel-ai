# import the opencv module
import cv2

from detection.object_detection_util import is_human_present

# capturing video
capture = cv2.VideoCapture(0)
count = 0
# setting the camera resolution and frame per second
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
capture.set(cv2.CAP_PROP_FPS, 10)

while capture.isOpened():
    # to read frame by frame
    _, img_1 = capture.read()
    _, img_2 = capture.read()
    count = count + 1
    # find difference between two frames
    diff = cv2.absdiff(img_1, img_2)

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
        if cv2.contourArea(contour) > 1000 and is_human_present(img_1):
            cv2.rectangle(img_1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imwrite('/usr/local/squirrel-ai/captured/motion{:d}.jpg'.format(count), img_1)
    # cv2.drawContours(img_1, contours, -1, (0, 255, 0), 2)

    # display the output
    # cv2.imwrite('/usr/local/squirrel-ai/captured/motion{:d}.jpg'.format(count), img_1)
    if cv2.waitKey(100) == 13:
        exit()
