import sys
import requests
import logging

logging.basicConfig(filename='/usr/local/squirrel-ai/logs/service.log',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %('
                           'funcName)s: %(message)s', level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
NOTIFICATION_URL = 'http://my-security.local:8087/notification?camera-id=GATE-CAMERA'

if len(sys.argv) == 2:
    logging.info(sys.argv[1])
    NOTIFICATION_URL = 'http://my-security.local:8087/notification?camera-id='+sys.argv[1]

data = requests.post(NOTIFICATION_URL, "General Camera Information")
