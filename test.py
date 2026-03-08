import requests
import threading

url = "http://LOAD_BALANCER_PUBLIC_IP:8000/test"

def send():
    while True:
        requests.get(url)

for i in range(20):
    threading.Thread(target=send).start()

