import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import jwt
import numpy as np

### AUTHENTICATION ###
try:
    print("Getting Authentication")
    account_url = "https://ACCOUNTNAME.blob.core.windows.net"
    default_credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    token = default_credential.get_token("https://storage.azure.com/.default")

    #decoded = jwt.decode(token.token, options={"verify_signature": False})

    #print(decoded["upn"])

    input_container_client = blob_service_client.get_container_client("inputs")
    output_container_client = blob_service_client.get_container_client("output")


except Exception as ex:
    print('ERROR:')
    print(ex)

### READ TEST ###

LOCAL_PATH = "./blob_test_download"
os.makedirs(LOCAL_PATH,exist_ok=True)
# blob client needs account url, container name, blob name 
#blob_client = BlobClient(account_url,"inputs","test_input.csv", credential=default_credential)
# blob_client = blob_service_client.get_blob_client(container="inputs",blob="test_input.csv")
# temp = blob_client.download_blob().read_all()
# print(f"\n temp type : {type(temp)}")
# print(f"temp value : {temp}\n")

## LIST BLOB NAMES ##
print("Reading contianer")
blob_list = input_container_client.list_blobs()
print(f"blob list: {blob_list}\n")
print(f"blob list type: {type(blob_list)}")
print("Print blob list")
for blob in blob_list:
    print("\t" + blob.name)
    download_path = os.path.join(LOCAL_PATH,"temp_" + blob.name)
    print("\nDownloading blob to \n\t" + download_path)
    processed_path = os.path.join(LOCAL_PATH,"processed_" + blob.name)
    temp = input_container_client.download_blob(blob.name).readall() 
    print(f"\n temp type : {type(temp)}")
    print(f"temp value : {temp}\n")
    str_arr = temp.decode('utf-8')
    print(f"\n str_arr type : {type(str_arr)}")
    print(f"str_arr value : {str_arr}\n")
    np_arr = np.array(str_arr.split(','),dtype=int)
    print(f"\n np_arr type : {type(np_arr)}")
    print(f"np_arr value : {np_arr}\n")
    sort_arr = np.sort(np_arr)
    print(f"\n sort_arr type : {type(sort_arr)}")
    print(f"sort_arr value : {sort_arr}\n")

    np.savetxt(processed_path, sort_arr.reshape(1,-1), delimiter=",", fmt="%d")


### WRITE TEST ###

