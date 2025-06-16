from flask import Flask, render_template, request

# Import the database object and models
from data_models import db, Author, Book

app = Flask(__name__)

# Create db object


# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the app to the SQLAlchemy object
db.init_app(app)

# Route to add an author
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']

        author = Author(
            name=name,
            birth_date=birth_date or None,
            date_of_death=date_of_death or None
        )
        db.session.add(author)
        db.session.commit()

    return render_template('')

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()