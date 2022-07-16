import sys
import requests
import logging

logging.basicConfig(filename='/usr/local/squirrel-ai/logs/notification.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %('
                           'funcName)s: %(message)s', level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("Inside the Analyze video notification having argument {}".format(len(sys.argv)))

if len(sys.argv) == 2:
    logging.info(sys.argv[1])
    NOTIFICATION_URL = 'http://my-security.local:5000/trigger-analysis'
    data = requests.post(NOTIFICATION_URL, data={'file': sys.argv[1]})
