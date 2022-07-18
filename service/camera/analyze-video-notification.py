import sys
import requests
import logging
import time

logging.basicConfig(filename='/usr/local/squirrel-ai/logs/notification.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %('
                           'funcName)s: %(message)s', level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("Analyze-Video-Notification")
if len(sys.argv) == 2:
    file_name = sys.argv[1]
    logger.info("Start : {0}".format(file_name))
    NOTIFICATION_URL = 'http://my-security.local:5000/trigger-analysis'
    start_time = time.time()
    data = requests.post(NOTIFICATION_URL, data={'file': file_name})
    logger.info(
        "End: {0}, Execution time : {1} seconds, Response: {2}".format(file_name, round(time.time() - start_time, 2) , data.reason))
