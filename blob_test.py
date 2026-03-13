import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import numpy as np

# local test to check python connection to Azure Storage Account. 

### AUTHENTICATION ###
try:
    print("Getting Authentication")
    # URL Format
        # storage account : "https://cst8911test.blob.core.windows.net"
        # container : "https://cst8911test.blob.core.windows.net/input"
        # blob : "https://cst8911test.blob.core.windows.net/input/test_input.csv"

    account_url = "https://8911midterm.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    input_container_client = blob_service_client.get_container_client("input")
    output_container_client = blob_service_client.get_container_client("output")


except Exception as ex:
    print('ERROR:')
    print(ex)

### READ TEST ###

LOCAL_PATH = "./blob_test_download"
os.makedirs(LOCAL_PATH,exist_ok=True)

## LIST BLOB NAMES ##
print("Reading contianer")
blob_list = output_container_client.list_blobs()
print(f"blob list: {blob_list}\n")
print(f"blob list type: {type(blob_list)}")
print("Print blob list")

# process each blob
processed_blob = ""
for blob in blob_list:
    print(f"blob list: {blob}\n")
    print(f"blob list type: {type(blob)}")
    print(f"\n{blob.name}")

    # create process filename
    processed_blob = "processed_" + blob.name
    processed_path = os.path.join(LOCAL_PATH,processed_blob)

    # get blob data
    temp = output_container_client.download_blob(blob.name).readall() 
    print(f"\n temp type : {type(temp)}")
    print(f"temp value : {temp}\n")

    # convert byte into string
    str_arr = temp.decode('utf-8')
    print(f"\n str_arr type : {type(str_arr)}")
    print(f"str_arr value : {str_arr}\n")

    # convert string into numpy int array
    np_arr = np.array(str_arr.split(','),dtype=int)
    print(f"\n np_arr type : {type(np_arr)}")
    print(f"np_arr value : {np_arr}\n")

    # sort array 
    sort_arr = np.sort(np_arr)
    print(f"\n sort_arr type : {type(sort_arr)}")
    print(f"sort_arr value : {sort_arr}\n")

    # save sorted array into csv file
    np.savetxt(processed_path, sort_arr.reshape(1,-1), delimiter=",", fmt="%d")
print("Done")

 ### WRITE TEST ###
print("UPLOADING BLOB")
new_blob = blob_service_client.get_blob_client(container="outputs",blob=processed_blob)
# Upload the created file
with open(file=processed_path, mode="rb") as data:
    new_blob.upload_blob(data) 