@echo off

call .venv\Scripts\activate

cd server
cd xakatonDRF

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
