#!/bin/bash

mkdir -p data
rm -f data/log.txt
touch data/log.txt
git pull
# inside python container
docker container run -w="/src/" -v $(pwd):/src/ -t python:3.10 /bin/bash -c "pip3 install -r requirements.txt; python3 main.py"