#!/bin/bash
# update packages
sudo apt update -y

sudo apt-get install python
pip install virtualenv



git clone https:GITLINK /web_app

cd /web_app
python -m venv .venv 

./venv/Scripts/activate
pip install -r requirements.txt

python ./vm_app.py