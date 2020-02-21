#!/bin/bash

pip install virtualenv
virtualenv -p python3 ../.env
../.env/bin/pip install -r requirements.txt
source ../.env/bin/activate 

