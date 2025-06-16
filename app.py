from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import the database object and models (we'll create these in data_models.py)
# from data_models import db, Author, Book

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the app to the SQLAlchemy object
# db.init_app(app)