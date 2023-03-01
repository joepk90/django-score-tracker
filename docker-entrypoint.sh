#!/bin/bash

# Collect static files
# echo "Collect static files"
# python manage.py collectstatic --noinput

# TODO it's bad that this runs every time the server starts... this needs to be conditional...
# Apply database migrations
echo "Apply database migrations for deployment"
python manage.py deploy

# Start server
echo "Starting server"
gunicorn --bind :$PORT score_tracker.wsgi:application