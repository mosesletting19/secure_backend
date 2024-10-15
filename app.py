import os  # Make sure to import os
from flask import Flask
from flask_cors import CORS  # Import CORS
from extensions import db, bcrypt, login_manager
from routes import auth_routes

def create_app():
    app = Flask(__name__)

    # Load config from .env or config file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

    # Enable CORS for the entire app
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_routes)

    return app

# Create the app
app = create_app()

# Push context manually to create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
