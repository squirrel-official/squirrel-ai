import cv2
import numpy as np
from cv2.gapi import kernel

from faceComparisonUtil import extract_face
from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import convolve2d as conv2, convolve2d

from skimage import color, data, restoration

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name


cap = cv2.VideoCapture('/usr/local/squirrel-ai/2.mkv')
count = 0
sec = 0
# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpen = cv2.filter2D(frame, -1, sharpen_kernel)
        face_image = extract_face(sharpen)
        if face_image is not None:
            cv2.imwrite('/usr/local/squirrel-ai/captured/frame{:d}.jpg'.format(sec), face_image)

        cv2.imwrite('/usr/local/squirrel-ai/captured/frame-sharp{:d}.jpg'.format(sec), sharpen)
        cv2.imwrite('/usr/local/squirrel-ai/captured/frame-raw{:d}.jpg'.format(sec), frame)

        kernal = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        image_sharp = cv2.filter2D(src=frame, ddepth=-1, kernel=kernel)
        cv2.imwrite('/usr/local/squirrel-ai/captured/frame-sharpened{:d}.jpg'.format(sec), image_sharp)

        ret, frame = cap.read()
        sec = sec + 1
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
