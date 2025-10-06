
from flask import Flask, render_template, request, flash,redirect, url_for, session
from app import create_app, db 
from app.model import Book, User
from app.forms import RegistrationForm, LoginForm

# Create Flask app and initialize MongoDB
app = create_app()

# Ensure Book collection is populated when app starts
with app.app_context():
    Book.initialize_collection()

##Code to clear db - for testing purposes only
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
        # Check if the email already exists
        if User.objects(email=form.email.data).first():
            flash(f"Email {form.email.data} already registered!", "danger")
            return render_template("register.html", form=form)
        
        # Save user to MongoDB
        new_user = User(
            email=form.email.data,
            password=form.password.data,  # optional: hash this
            name=form.name.data,
        )
        new_user.save()
        flash(f"Registration successful for {form.email.data}!", "success")
        return redirect(url_for('book_titles'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if user exists
        user = User.objects(email=form.email.data).first()
        if not user:
            flash("Email not registered!", "danger")
            return render_template("login.html", form=form)

        # Check password
        if user.password != form.password.data:
            flash("Incorrect password!", "danger")
            return render_template("login.html", form=form)
        
        # Login successful: set session variables
        session['user_email'] = user.email
        session['user_name'] = user.name
        
        # Remember Me
        if form.remember.data:  # Remember Me checked
            session.permanent = True
        else:
            session.permanent = False  # Log out when browser closes

        flash(f"Welcome {user.name}!", "success")
        return redirect(url_for('book_titles'))

    return render_template("login.html", form=form)



@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_name', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('book_titles'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)