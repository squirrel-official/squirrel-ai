import sys
import requests
import logging

logging.basicConfig(filename='/usr/local/squirrel-ai/logs/notification.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %('
                           'funcName)s: %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
NOTIFICATION_URL = 'http://my-security.local:8087/notification?camera-id=GATE-CAMERA'
logger = logging.getLogger("Motion-Detection-Notification")
if len(sys.argv) == 2:
    NOTIFICATION_URL = 'http://my-security.local:8087/notification?camera-id='+sys.argv[1]

logger.info("Notification: {}".format(NOTIFICATION_URL))
requests.post(NOTIFICATION_URL, "General Camera Information")
