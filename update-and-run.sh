#!/bin/bash
git pull
# inside python container
docker container run -w="/src/" -v /media/apps/investing/:/src/ -t python:3.10 /bin/bash -c "pip3 install -r requirements.txt; python3 main.py"