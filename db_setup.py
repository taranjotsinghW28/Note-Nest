# db_setup.py
from app import create_app, db
import os

def setup_db():
    # Set the DATABASE_URL environment variable for the script to use
    os.environ['DATABASE_URL'] = os.getenv('DATABASE_URL')
    
    app = create_app()
    with app.app_context():
        # Create tables only if they don't exist
        db.create_all()
        print("Database tables created successfully!")

if __name__ == "__main__":
    setup_db()