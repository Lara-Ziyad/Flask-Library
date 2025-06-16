from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import the database object and models (we'll create these in data_models.py)
# from data_models import db, Author, Book

app = Flask(__name__)

# Create db object
db = SQLAlchemy()

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the app to the SQLAlchemy object
db.init_app(app)

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()