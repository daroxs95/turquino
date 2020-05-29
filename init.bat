@echo off
Title djangoSERVER
python manage.py makemigrations && python manage.py migrate && python manage.py runserver
