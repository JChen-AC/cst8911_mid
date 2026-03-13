from flask import Flask, jsonify, request, abort
import time
import socket 
import os
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import numpy as np

## Flask server to handle the data processing 

## Variables 
OUTPUT_CONTAINER = "outputs"
INPUT_CONTAINER = "inputs"
storage_account1 = "https://cst8911test.blob.core.windows.net"
storage_account2 = "https://8911midterm.blob.core.windows.net"


## Authenticate 
try:
    print("Getting Authentication")
    account_url = storage_account1    
    # get authentication credentials
    default_credential = ManagedIdentityCredential() # get only the managed identity credentials 
    #default_credential = DefaultAzureCredential() # use the default credential method, which can get a varierty of credentials
    
    # create storage account and container clients
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    input_container_client = blob_service_client.get_container_client(INPUT_CONTAINER)
    output_container_client = blob_service_client.get_container_client(OUTPUT_CONTAINER)


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
## CPU test that is used to simulate heavy cpu usage 
@app.route('/cpu_test',methods=['GET'])
def cpu_test():
    # count to a large number
    total = 0
    for i in range(10**9):
        total += i
    
    return jsonify({"message":f"CPU Test completed : serveved by {socket.gethostname()}"}),201

## blob test that is used to test the storage account and python connection
# gets the all the blobs in the input container, gets the data from them, processes them and uploads them to the output container
@app.route('/blob_test',methods=['GET'])
def blob_test():    
    try:
        LOCAL_PATH = "./blob_test_download"
        os.makedirs(LOCAL_PATH,exist_ok=True)

        ## GET BLOBS ##
        print("Reading contianer")
        blob_list = input_container_client.list_blobs()

        ## Processes Blobs ## 
        processed_blob = ""
        for blob in blob_list:
            # create filename
            processed_blob = "processed_" + blob.name
            processed_path = os.path.join(LOCAL_PATH,processed_blob)

            # get blob data and processes it 
            blob_data = input_container_client.download_blob(blob.name).readall() # get file data (in bytes)
            str_arr = blob_data.decode('utf-8') # convert data to string 
            np_arr = np.array(str_arr.split(','),dtype=int) # convert string to numpy int array
            sort_arr = np.sort(np_arr) # sort array
            np.savetxt(processed_path, sort_arr.reshape(1,-1), delimiter=",", fmt="%d") #save sorted array into csv file

        ### WRITE TEST ###
        print("UPLOADING BLOB")
        new_blob = blob_service_client.get_blob_client(container=OUTPUT_CONTAINER,blob=processed_blob)
        # Upload the created file
        with open(file=processed_path, mode="rb") as data:
            new_blob.upload_blob(data)
        os.remove(processed_path)

        return jsonify({"message":f"Blob Test completed : uploaded file {processed_path} to output container, serveved by {socket.gethostname()}"}),202
    except Exception as ex:
        print('ERROR:')
        print(ex)
        return jsonify({"ERROR":f"Blob test failed :error caused by {str(ex)}"}),502

## Blob read test to test storage account and python connection
# connects to the input container and gets the names of all the blob files
@app.route('/blob_read',methods=['GET'])
def blob_read():    
    ## LIST BLOB NAMES ##
    print("Reading contianer")
    blob_list = input_container_client.list_blobs()
    blobs = [blob.name for blob in input_container_client.list_blobs()]

    return jsonify({"message":f"Blob Read Test completed : {blobs}"}),205

## azure data factory (ADF) test to get the json inputs from the web request 
# used to test the web activity in the azure data factory to see if it is properly sending the data
@app.route('/adf', methods=['POST'])
def adf_test():
    # gets the data from the body of the request and returns them
    inputs_data = request.json    
    return jsonify(inputs_data), 203  # Return HTTP status 203 OK

## azure data factory and account storage test
# gets the input filename from the azure data factory and uses the file name to get the information, processes it and stores it in the output container
@app.route('/adf_blob', methods=['POST'])
def adf_blob_test():
    # get input filename
    inputs_data = request.json 
    filename = inputs_data["filename"]

    try:
        #make file path 
        LOCAL_PATH = "./blob_test_download"
        os.makedirs(LOCAL_PATH,exist_ok=True)        
        processed_blob = "processed_" + filename
        processed_path = os.path.join(LOCAL_PATH,processed_blob)

        # get the input file information and process it 
        blob_client = input_container_client.get_blob_client(filename)
        blob_data = blob_client.download_blob().readall() # get file data (in bytes)
        str_arr = blob_data.decode('utf-8') # convert data to string 
        np_arr = np.array(str_arr.split(','),dtype=int) # convert string to numpy int array
        sort_arr = np.sort(np_arr) # sort array
        np.savetxt(processed_path, sort_arr.reshape(1,-1), delimiter=",", fmt="%d") #save sorted array into csv file
    except Exception as ex:
        # print output error and return the error if something fails with getting and processing the information
        print('ERROR:')
        print(ex)
        return jsonify({"ERROR":f"ADF Blob test failed when trying to read blob: error caused by {str(ex)}"}),503
    try:
        ### WRITE PROCESSED DATA ###
        print("UPLOADING BLOB")
        # create a new blob client that will be the blob that is uploaded to the container
        new_blob = blob_service_client.get_blob_client(container=OUTPUT_CONTAINER,blob=processed_blob)
        # Upload the created file
        with open(file=processed_path, mode="rb") as data:
            new_blob.upload_blob(data) # Reads the data from the saved csv and uploads it to the blob
        os.remove(processed_path) # remove the local process file once it has been uploaded

        return jsonify({"message":f"ADF and Blob Test completed : uploaded file {processed_path} to output container, serveved by {socket.gethostname()}"}),201
    except Exception as ex:
        # print output error and return the error if something fails with uploading to output container 
        print('ERROR:')
        print(ex)
        return jsonify({"ERROR":f"Blob test failed when trying to write to blob:error caused by {str(ex)}"}),504

## Full test that does the simulates cpu usage as well as receiving and processing information and uploading it to the output container
@app.route('/full_test', methods=['POST'])
def full_test():
    ## get input values 
    inputs_data = request.json 
    filename = inputs_data["filename"]

    ## simulate cpu usage 
    total = 0
    for i in range(10**9):
        total += i 

    ## Process and upload information
    try:
        #make file path 
        LOCAL_PATH = "./blob_test_download"
        os.makedirs(LOCAL_PATH,exist_ok=True)
        processed_blob = "processed_" + filename
        processed_path = os.path.join(LOCAL_PATH,processed_blob)

        # get the input file information and process it 
        blob_data = input_container_client.download_blob(filename).readall() # get file data (in bytes)
        str_arr = blob_data.decode('utf-8') # convert data to string 
        np_arr = np.array(str_arr.split(','),dtype=int) # convert string to numpy int array
        sort_arr = np.sort(np_arr) # sort array
        np.savetxt(processed_path, sort_arr.reshape(1,-1), delimiter=",", fmt="%d") #save sorted array into csv file

        ### WRITE PROCESSED DATA ###
        print("UPLOADING BLOB")

        # create a new blob client that will be the blob that is uploaded to the container
        new_blob = blob_service_client.get_blob_client(container=OUTPUT_CONTAINER,blob=processed_blob)

        # Upload the created file
        with open(file=processed_path, mode="rb") as data:
            new_blob.upload_blob(data) # Reads the data from the saved csv and uploads it to the blob
        os.remove(processed_path) # remove the local process file once it has been uploaded

        return jsonify({"message":f"Full Test completed : uploaded file {processed_path} to output container, serveved by {socket.gethostname()}"}),206
    except Exception as ex:
        print('ERROR:')
        print(ex)
        return jsonify({"ERROR":f"Blob test failed :error caused by {str(ex)}"}),502


# Entry point for running the Flask app
# The app will run on host 0.0.0.0 (accessible on all network interfaces) and port 8000.
# Debug mode is disabled (set to False).
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
