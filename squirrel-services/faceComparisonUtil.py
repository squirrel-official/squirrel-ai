import logging
from random import randint
import sys
import os
import traceback
import cv2
from PIL import Image

import face_recognition
from face_recognition import load_image_file, face_encodings


def compare_faces(known_image_path, unknown_image_path):
    # known_image = face_recognition.load_image_file("/Users/anil/Desktop/saurabh.jpeg")
    known_image = load_image_file(known_image_path)
    known_encoding = face_encodings(known_image)[0]

    # image = face_recognition.load_image_file("/Users/anil/Desktop/test1.png")
    image = load_image_file(unknown_image_path)
    face_locations = face_recognition.face_locations(image)

    for face_location in face_locations:

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        logging.debug(
            "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                  right))

        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        unknown_encoding = face_recognition.face_encodings(face_image)[0]
        face_compare_list = face_recognition.compare_faces([unknown_encoding], known_encoding)
        # show the image if it  has matched
        for face_compare in face_compare_list:
            if face_compare:
                pil_image.show()


def extract_faces(image, count):
    face_locations = face_recognition.face_locations(image)

    for face_location in face_locations:
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                                                                                                    right))
        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        cv2.imwrite('/Users/anil/Desktop/test/frame{:d}.jpg'.format(count), face_image)
        # pil_image.show()

