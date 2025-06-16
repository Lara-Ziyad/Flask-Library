from flask import Flask, render_template, request
from data_models import db, Author, Book
import os
from datetime import datetime

app = Flask(__name__)


# Database config

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the app to the SQLAlchemy object
db.init_app(app)

# Route to add an author
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')

        # Convert the form input strings to datetime.date
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

        author = Author(
            name=name,
            birth_date=birth_date or None,
            date_of_death=date_of_death or None
        )
        db.session.add(author)
        db.session.commit()
        return "Author added successfully", 201

    return "Use POST to add an author", 200

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()

    app.run(debug=True)