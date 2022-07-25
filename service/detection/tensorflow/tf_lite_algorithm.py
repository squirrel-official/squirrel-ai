"""Main script to run the object detection routine."""

import cv2

from detection.tensorflow.object_detector import ObjectDetector
from detection.tensorflow.object_detector import ObjectDetectorOptions
from detection.tensorflow.utils import visualize


def perform_object_detection(image, model: str, enable_edgetpu: bool) -> None:
    """Continuously run inference on images acquired from the camera.

  Args:
    model: Name of the TFLite object detection model.
    num_threads: The number of CPU threads to run the model.
    enable_edgetpu: True/False whether the model is a EdgeTPU model.
  """

    # Initialize the object detection model
    options = ObjectDetectorOptions(
        num_threads=4,
        score_threshold=0.3,
        max_results=3,
        enable_edgetpu=enable_edgetpu)
    detector = ObjectDetector(model_path=model, options=options)

    # Continuously capture images from the camera and run inference

    image = cv2.flip(image, 1)

    # Run object detection estimation using the model.
    detections = detector.detect(image)

    # Draw points and edges on input image
    return visualize(image, detections)
