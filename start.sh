#!/bin/bash

# Install dependencies if needed
pip install --user -r requirements.txt

# Set environment variables
export FLASK_APP=app/app.py
export PYTHONPATH=.
export FLASK_ENV=development

# Run the app
flask run --host=0.0.0.0 --port=5000
