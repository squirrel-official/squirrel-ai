import requests

NOTIFICATION_URL = 'http://my-security.local:8087/notification?camera-id=3'
data = requests.post(NOTIFICATION_URL, "General Camera Information")
