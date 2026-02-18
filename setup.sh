#!/bin/bash
set -ex
# update packages
sudo apt update -y

sudo apt install python3-pip -y
sudo apt install python3.12-venv -y
sudo apt install git -y

mkdir app
cd ./app

git clone web_app

cd ./web_app
python3 -m venv .venv 

source ./.venv/bin/activate
pip install -r requirements.txt

nohup python ./vm_app.py > flask.log >2>&1 &

# HOW DOES IT HANDLE ASKING FOR USER PASSWORD