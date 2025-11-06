# wsgi.py
# This file tells Gunicorn how to import and run your Flask app.

from app import create_app

# The 'app' variable must be globally available for Gunicorn
app = create_app()