import requests
import threading

url = "http://LOAD_BALANCER_PUBLIC_IP:8000/test"

def send():
    response = None
    while response is None:
        response = requests.get(url)

for i in range(20):
    print(f"Creating thread: {i}")
    threading.Thread(target=send).start()

