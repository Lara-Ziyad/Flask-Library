from flask import Flask, render_template, request, flash
from data_models import db, Author, Book
import os
from datetime import datetime
import requests
from requests.exceptions import RequestException 
app = Flask(__name__)


# Database config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # For flash messages

# Bind the app to the SQLAlchemy object
db.init_app(app)

# Helper function to fetch cover
def get_cover_url_from_isbn(isbn):
    return f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        birth_date_str = request.form.get('birth_date')
        date_of_death_str = request.form.get('date_of_death')

        # Convert the form input strings to datetime.date
        birth_date = datetime.strptime(birth_date_str, '%m.%d.%Y').date() if birth_date_str else None
        date_of_death = datetime.strptime(date_of_death_str, '%m.%d.%Y').date() if date_of_death_str else None

        author = Author(
            name=name,
            birth_date=birth_date or None,
            date_of_death=date_of_death or None
        )
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!')

    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author_id = request.form.get('author_id')
        isbn = request.form.get('isbn', '').strip()

        if not title:
            flash("Title is required!")
        else:
            cover_url = get_cover_url_from_isbn(isbn) if isbn else None

            book = Book(
                title=title,
                author_id=int(author_id) if author_id else None,
                isbn=isbn,
                cover_url=cover_url
            )
            db.session.add(book)
            db.session.commit()
            flash('Book added successfully!')

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)



# Route to search book
@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.args.get('search', '').strip()
    sort_option = request.args.get('sort', 'title')

    query = Book.query.outerjoin(Author)

    # Apply search
    if request.args.get('search') is not None:
        if search_query:
            query = query.filter(Book.title.ilike(f'%{search_query}%'))
        else:
            flash('Please enter a search term!')

    # Apply sorting
    if sort_option == 'author':
        query = query.order_by(Author.name.asc())
    else:
        query = query.order_by(Book.title.asc())

    books = query.all()

    if search_query and not books:
        flash('No books found matching your search!')

    return render_template('home.html', books=books, search_query=search_query, sort_option=sort_option)



if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()

    app.run(debug=True)