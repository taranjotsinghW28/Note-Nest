from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "my_super_secret_key")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", 
        "sqlite:///note_nest_dyh0.db"
    ).replace("postgres://", "postgresql://")
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.signin"
    login_manager.login_message_category = "info"

    # Import and register blueprints
    from .routes.auth import auth_bp
    from .routes.task import note_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(note_bp)

    # Import models and create database tables if they don’t exist
    from .models import User, Note
    with app.app_context():
        db.create_all()

    return app


# Load user for Flask-Login
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))