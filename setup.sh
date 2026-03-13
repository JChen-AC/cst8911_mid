#!/bin/bash
set -ex
# update packages
sudo apt update -y

# install python and git
sudo apt install python3-pip -y
sudo apt install python3.12-venv -y
sudo apt install git -y

# make directory to install repository
mkdir app
cd ./app

# Clone repository
git clone https://github.com/JChen-AC/cst8911_mid.git

# go into the repository
cd cst8911_mid

# create a virtual environment and download the requirements 
python3 -m venv .venv 
source ./.venv/bin/activate
pip install -r requirements.txt

# run the flask server in the background and log the outputs
nohup python ./vm_app.py > flask.log 2>&1 &