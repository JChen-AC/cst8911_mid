# create a flask server
# server will accept some input 
# server will then print something 
# server will then sleep for a bit (simulate processing)
# server will print something again 
# server will be ready to accept the next request 
# maybe print something is actually sending the request somewhere else? 

from flask import Flask, jsonify, request, abort
import time
import socket 
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import numpy as np

try:
    print("Getting Authentication")
    account_url = "https://cst8911test.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    token = default_credential.get_token("https://storage.azure.com/.default")
    input_container_client = blob_service_client.get_container_client("inputs")
    output_container_client = blob_service_client.get_container_client("outputs")


except Exception as ex:
    print('ERROR:')
    print(ex)

app = Flask(__name__)

# Define route to handle requests to the root URL ('/')
@app.route('/')
def index():
    return "VMSS Test App! "

# Health check route (GET)
# This endpoint returns a 200 OK status and a JSON response to confirm that the service is running.
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200  # Return HTTP status 200 OK

# Send process request 
@app.route('/test',methods=['GET'])
def cpu_test():
    
    total = 0
    for i in range(10**9):
        total += i
    
    return jsonify({"message":f"CPU Test completed : serveved by {socket.gethostname()}"}),201

# Send process request 
@app.route('/blob_test',methods=['GET'])
def blob_test():
    try:
        LOCAL_PATH = "./blob_test_download"
        os.makedirs(LOCAL_PATH,exist_ok=True)

        ## LIST BLOB NAMES ##
        print("Reading contianer")
        blob_list = input_container_client.list_blobs()
        processed_blob = ""
        for blob in blob_list:
            processed_blob = "processed_" + blob.name
            processed_path = os.path.join(LOCAL_PATH,processed_blob)
            temp = input_container_client.download_blob(blob.name).readall() 
            str_arr = temp.decode('utf-8')
            np_arr = np.array(str_arr.split(','),dtype=int)
            sort_arr = np.sort(np_arr)
            np.savetxt(processed_path, sort_arr.reshape(1,-1), delimiter=",", fmt="%d")

        ### WRITE TEST ###
        print("UPLOADING BLOB")
        new_blob = blob_service_client.get_blob_client(container="outputs",blob=processed_blob)
        # Upload the created file
        with open(file=processed_path, mode="rb") as data:
            new_blob.upload_blob(data)
        os.remove(processed_path)

        return jsonify({"message":f"Blob Test completed : serveved by {socket.gethostname()}"}),201
    except Exception as ex:
        print('ERROR:')
        print(ex)
        return jsonify({"ERROR":f"Blob test failed :error caused by {ex}"}),502

    


# Entry point for running the Flask app
# The app will run on host 0.0.0.0 (accessible on all network interfaces) and port 8000.
# Debug mode is disabled (set to False).
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
