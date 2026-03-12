#!/bin/bash
set -ex
# update packages
sudo apt update -y

sudo apt install python3-pip -y
sudo apt install python3.12-venv -y
sudo apt install git -y

mkdir app
cd ./app

# Clone repository
git clone https://github.com/JChen-AC/cst8911_mid.git

cd cst8911_mid

python3 -m venv .venv 

source ./.venv/bin/activate
pip install -r requirements.txt

nohup python ./vm_app.py > flask.log 2>&1 &