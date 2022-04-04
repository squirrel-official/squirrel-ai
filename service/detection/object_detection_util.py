import cv2


def is_human_present(hog, image):
    bounding_box_coordinates, weights = hog.detectMultiScale(image, winStride=(4, 4), padding=(4, 4), scale=1.05)
    person = 0
    for x, y, w, h in bounding_box_coordinates:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        person += 1

    if person > 0:
        return True
    else:
        return False
