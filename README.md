# CST8911 Midterm Project: Data Factory Pipeline (Scenario 3)

## Files and Folders

### test_scripts 
This folder contains the test input csv files that were used to test the datafactory pipeline. They consist of a series of numbers that will be sorted by the pipeline.

### blob_test.py
Used to test the Azure Python libraries to test how they work and to ensure that he code works properly. This test runs locally using Az CLI to provide the credentials. It connects to the Azure Storage Account and gets all the blobs inside the input container. It then gets the data and processes the data for each of the blob, sorting the values from lowest to highest and saving it to a csv file. 
It then uploads the csv file to the Output container. 

### process_script.py
An alternative process script that was not used. This is a python script that would be started up through Azure Datafactory Pipeline which sends a POST request to a VM instance to run this script. It gets the filename from the pipeline, finds the Blob in the Storage Account, gets the information, processes it and uploads the process information to the Output container. 
This was not chosen due to the script bypassing the Load balancer. The pipeline triggers a Post request that is used to do a VM run command, however this requires the request to be sent directly to the VM and can't be passed through the load balancer. Which is why we chose not to use it. 

### requirements.txt
A list of python libraries needed to be installed for the application to work 

### setup.sh
A bash script that is used for the Custom Script Extension that Azure Virtual Machine Scale Sets offers. It is executed when a virtual machine (VM) instance is created and is used to install all the dependencies, get the code from GitHub and run the application

### start_cpu_test.py
This script is used to simulate heavy traffic on the Flask server on the VM. It automatically creates a bunch of threads that send request to the /test route of the Flask server. With the /test route being used to simulate heavy cpu usage

### vm_app.py
This is the Flask server that is loaded onto the VM instances. It is downloaded and started using the setup.sh script. It uses the Azure libraires to get the authentication and connect to the Azure Storage Account and the input and output containers. 
There are a series of routes used for different test 


| Route | description|
| ---- | ----| 
| / | root route, to hanlde request to the root URL |
| /health | Health check to see if you can connect to the Flask server | 
| /cpu_test | Simulates heavy CPU usage by counting to a very large number (10^9) |
| /blob_test| Used to test the storage account and python connection, getting all the blobs from input container, getting their data, processing it and then uploading the process data to the output container |
| /blob_read | Secondary test to test he storage account and python connectin, specifically the ipnut container connection and the managed identities. Gets all the blob filenames and returns them |
| /adf | Azure Datafactory test to test the Pipeline's POST request body data that is sent by the Web Activity request to ensure that the data is properly transfered | 
| /adf_blob | Azure Datafactory and Storage account test. Combining the Blob_test and adf test, where it uses the datafactory pipeline to trigger the route, passing in the filename to get the information. Then it processes it and uploads the processed data to the Output Container | 
| /full_test | Combines the adf_blob test and cpu_test, adding the simulated cpu usage to the adf_blob code | 
