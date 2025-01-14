#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input


python manage.py migrate --noinput

# Crée un super utilisateur (en utilisant des variables d'environnement)
#python manage.py createsuperuser --noinput \
 #   --username Donatien \
  #  --email donaerickoulodji@gmail.com || true \
   # --password erick0151 || true
# Apply any outstanding database migrations
#python manage.py migrate