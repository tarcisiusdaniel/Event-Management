#!/bin/sh



pip3 install --root-user-action=ignore -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000