import cv2
import glob
from datetime import datetime

from face_recognition import load_image_file, face_encodings

from faceComparisonUtil import extract_face, compare_faces

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(0)
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
        face_image = extract_face(frame)
        # print(glob.glob("/usr/local/squirrel-ai/wanted-criminals/*"))
        if face_image is not None:
            # saving the image to visitor folder
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            cv2.imwrite('/usr/local/squirrel-ai/visitor/'+timestamp+'.jpg', frame)
            for eachWantedCriminalPath in glob.glob('/usr/local/squirrel-ai/wanted-criminals/*'):
                criminal_image = load_image_file(eachWantedCriminalPath)
                criminal_image_encoding = face_encodings(criminal_image)[0]
                # print(eachWantedCriminalPath)
                if compare_faces(criminal_image_encoding, face_image, eachWantedCriminalPath):
                    cv2.imwrite('/usr/local/squirrel-ai/captured/frame{:d}.jpg'.format(sec), face_image)
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
