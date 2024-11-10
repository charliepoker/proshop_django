#!/bin/bash

if [ "$1" = "test" ]; then
    echo "Running tests..."
    python manage.py test base.tests
else
    echo "Starting server..."
    python manage.py runserver 0.0.0.0:8000
fi

