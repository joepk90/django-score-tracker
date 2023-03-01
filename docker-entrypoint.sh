#!/bin/bash

# Collect static files
# echo "Collect static files"
# python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations for deployment"
python manage.py deploy

# Start server
echo "Starting server"
gunicorn --bind :$PORT score_tracker.wsgi:application