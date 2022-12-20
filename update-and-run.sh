#!/bin/bash

mkdir -p data
git pull
pip3 install -r requirements.txt
python3 main.py > data/log.txt