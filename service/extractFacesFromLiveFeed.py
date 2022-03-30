import cv2
import glob
import logging
from datetime import datetime

from face_recognition import load_image_file, face_encodings

from faceComparisonUtil import extract_face, extract_unknown_face_encodings, compare_faces_with_encodings

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(0)
count = 0
sec = 0
criminal_cache = []
# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

# setting the camera resolution and frame per second
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 10)

startDateTime = datetime.now()
for eachWantedCriminalPath in glob.glob('/usr/local/squirrel-ai/wanted-criminals/*'):
    criminal_image = load_image_file(eachWantedCriminalPath)
    criminal_image_encoding = face_encodings(criminal_image)[0]
    criminal_cache.append(criminal_image_encoding)

endDateTime = datetime.now()
# Once the loading is done then print
print("Loaded {0} images in {1} seconds".format(len(criminal_cache), (endDateTime - startDateTime)))

# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        unknown_face_image = extract_face(frame)
        if unknown_face_image is not None:
            unknown_face_image_encodings = extract_unknown_face_encodings(unknown_face_image)
            # saving the image to visitor folder
            startDateTime = datetime.now()
            startTimestampStr = startDateTime.strftime("%Y%m%d-%H%M%S")
            cv2.imwrite('/usr/local/squirrel-ai/visitor/' + startTimestampStr + '.jpg', frame)
            for each_criminal_encoding in criminal_cache:
                if compare_faces_with_encodings(each_criminal_encoding, unknown_face_image_encodings,
                                                "eachWantedCriminalPath"):
                    cv2.imwrite('/usr/local/squirrel-ai/captured/frame{:d}.jpg'.format(sec), unknown_face_image)
            endDateTime = datetime.now()
            print("Total comparison time is {0} seconds".format((endDateTime - startDateTime)))
            count = 3
            sec += 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, count)

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
