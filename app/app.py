
from flask import Flask, render_template, request, flash,redirect, url_for, session
from app import create_app, db 
from app.model import Book, User
from app.forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.forms import NewBookForm


# Create Flask app and initialize MongoDB
app = create_app()



login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

# Ensure Book collection is populated when app starts
with app.app_context():
    Book.initialize_collection()

#Code to clear db - for testing purposes only
# @app.route("/clear_db")
# def clear_books():
#     # Only for development/testing!
#     Book.objects.delete()
#     return "All books deleted from the database."


# ----------------------------------------------------------------------------------
# --- FEATURE 1: Search/Filter (Book Titles Page) ---
# ----------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/book_titles', methods=['GET'])
def book_titles():
    # Get selected category from dropdown
    current_category = request.args.get('category', 'All')

    # Use the database method. This method should handle filtering AND sorting.
    # We will update Book.find_by_category to handle sorting.
    filtered_books = Book.find_by_category(current_category) 
    
    # REMOVE: Python-based sorting is no longer necessary if DB does it.
    # sorted_books = filtered_books 

    return render_template(
        'book_titles.html',
        # Pass the already sorted results
        all_books=filtered_books, 
        current_category=current_category 
    )

# ----------------------------------------------------------------------------------
# --- FEATURE 2: Book Details Page (Retrieval) ---
# ----------------------------------------------------------------------------------
@app.route('/book_details/<book_title>')
def book_details(book_title):
    # Use MongoDB method to find book by title
    the_book = Book.find_by_title(book_title)

    if not the_book:
        return "Book not found", 404

    return render_template(
        'book_details.html',
        book=the_book
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        if User.objects(email=form.email.data).first():
            flash(f"Email {form.email.data} already registered!", "danger")
            return render_template("register.html", form=form)
        
        new_user = User(
            email=form.email.data,
            name=form.name.data
        )
        new_user.set_password(form.password.data)
        new_user.save()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if not user:
            flash("Email not registered!", "danger")
            return render_template("login.html", form=form)
        
        if not user.check_password(form.password.data):
            flash("Incorrect password!", "danger")
            return render_template("login.html", form=form)
        
        login_user(user, remember=form.remember.data)
        return redirect(url_for('book_titles'))

    return render_template("login.html", form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('book_titles'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = NewBookForm()

    if form.validate_on_submit():
        # Collect authors, adding "(Illustrator)" if checked
        authors = []
        for i in range(1, 6):
            name = getattr(form, f"author{i}").data
            if name:
                if getattr(form, f"illustrator{i}").data:
                    name += " (Illustrator)"
                authors.append(name)

        # Description as list (split by lines)
        description = [line.strip() for line in form.description.data.splitlines() if line.strip()]

        # Genres as list (SelectMultipleField returns a list already)
        genres = form.genres.data

        # Create and save book
        book = Book(
            title=form.title.data,
            category=form.category.data,
            genres=genres,
            url=form.url.data,
            description=description,
            authors=authors,
            pages=form.pages.data,
            copies=form.copies.data
        )
        book.save()

        # Flash message and remain on the same page
        flash("Book added successfully!", "success")
        return redirect(url_for('add_book'))  # stay on same page

    return render_template('add_book.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5000)