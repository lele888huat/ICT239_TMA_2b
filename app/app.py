# app.py - Main Flask Application (Controller Component) for Q2b

from flask import Flask, render_template, request
from app import create_app, db
from model import Book

# Create Flask app and initialize MongoDB
app = create_app()

# Ensure Book collection is populated when app starts
with app.app_context():
    Book.initialize_collection()


# --- Helper Function ---
# Function to sort books by title
def sort_books(books):
    return sorted(books, key=lambda book: book['title'])


# --- Book Titles Page (Handles Initial Load and Category Filtering) ---
@app.route('/', methods=['GET'])
@app.route('/book_titles', methods=['GET'])
def book_titles():
    # Get selected category from dropdown
    current_category = request.args.get('category', 'All')

    # Use MongoDB methods instead of all_books list
    filtered_books = Book.find_by_category(current_category)
    sorted_books = sort_books(filtered_books)

    return render_template(
        'book_titles.html',
        all_books=sorted_books,
        current_category=current_category  # Keep dropdown selection
    )


# --- Book Details Page ---
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
