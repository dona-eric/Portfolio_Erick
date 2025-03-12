#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files

python manage.py makemigrations
python manage.py migrate --noinput

# to colletc the staticfiles of images and data
python manage.py collectstatic --noinput
## to apply the migrations and execute them in the database
python manage.py migrate
