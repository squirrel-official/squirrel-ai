import time
from absl import app, flags, logging
from absl.flags import FLAGS
import cv2

import tensorflow as tf
from yolov3_tf2.models import (YoloV3, YoloV3Tiny)
from yolov3_tf2.dataset import transform_images
from yolov3_tf2.utils import draw_outputs
import datetime
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

flags.DEFINE_string('classes', './data/labels/coco.names', 'path to classes file')
flags.DEFINE_string('weights', './weights/yolov3.tf',
                    'path to weights file')
flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_string('video', './data/video/paris.mp4',
                    'path to video file or number for webcam)')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_integer('num_classes', 80, 'number of classes in the model')

song = AudioSegment.from_wav("1.wav")


def yolov3(image):
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    if FLAGS.tiny:
        yolo = YoloV3Tiny(classes=FLAGS.num_classes)
    else:
        yolo = YoloV3(classes=FLAGS.num_classes)

    yolo.load_weights(FLAGS.weights)
    logging.info('weights loaded')

    class_names = [c.strip() for c in open(FLAGS.classes).readlines()]
    logging.info('classes loaded')

    img_in = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_in = tf.expand_dims(img_in, 0)
    img_in = transform_images(img_in, FLAGS.size)

    t1 = time.time()
    boxes, scores, classes, nums = yolo.predict(img_in)

    img = draw_outputs(image, (boxes, scores, classes, nums), class_names)

    # cv2.resizeWindow('output', 300,300)

    print("the number of objects: {}".format(int(nums)))  # number of objects
    print(datetime.datetime.now())  # time of detections
    print('detection objects: ')  # class of objects
    for i in range(nums[0]):
        print('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
                                    np.array(scores[0][i]),
                                    np.array(boxes[0][i])))
        if (class_names[int(classes[0][i])]) == "person":  # filter for humans
            print("yes, human detected ")
            play(song)



