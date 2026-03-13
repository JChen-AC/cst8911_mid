import requests
import threading

# This script creates a bunch of threads and sends http request to the test route, to simulate traffic and trigger scaling

url = "http://20.104.33.111:8000/test"

def send():
    response = None
    while response is None:
        response = requests.get(url)

for i in range(30):
    print(f"Creating thread: {i}")
    threading.Thread(target=send).start()

