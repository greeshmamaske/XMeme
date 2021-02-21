#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3.7
sudo apt-get install -y python3-pip
sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y libpq-dev
pip3 install -r requirements.txt