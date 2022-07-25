import cv2

from customLogging.customLogging import get_logger
import os

logger = get_logger("Motion Detection")
ARCHIVE_URL = "/usr/local/squirrel-ai/data/archives/"


def archive_file(each_video_url):
    logger.info("Archiving {0}".format(each_video_url))
    file_name = os.path.basename(each_video_url)
    os.rename(each_video_url, ARCHIVE_URL + file_name)


def extract_blur(image, file_name):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    logger.debug(
        "blur ratio {0} for {1}".format(fm, file_name))