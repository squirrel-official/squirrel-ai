import cv2
import face_recognition
from faceComparisonUtil import extract_face

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('/Users/anil/Desktop/1.mp4')
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
        cv2.imwrite('/Users/anil/Desktop/ai/captured/frame{:d}.jpg'.format(sec), face_image)
        count += 30  # i.e. at 30 fps, this advances one second
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
