# app.py - Main Flask Application (Controller Component)

from flask import Flask, render_template, request
# Import the list of books from books.py
from books import all_books

app = Flask(__name__) 


# --- Helper Function ---
# Function to sort the book list by title
def sort_books(books):
    return sorted(books, key=lambda book: book['title'])

# Function to find a book by its title
def get_book_details(title):
    for book in all_books:
        if book['title'] == title:
            return book
    return None

# --- Book Titles Page (Handles Initial Load and Category Filtering) ---
@app.route('/', methods=['GET'])
@app.route('/book_titles', methods=['GET'])
def book_titles():

 
    current_category = request.args.get('category', 'All')
    
    if current_category != 'All':
        filtered_books = [
            book for book in all_books if book['category'] == current_category
        ]
    else:
        # If 'All', use the full list
        filtered_books = all_books
    
    sorted_books = sort_books(filtered_books)
    
    return render_template(
        'book_titles.html',
        all_books=sorted_books,
        current_category=current_category # <-- Fixes the dropdown reset issue
    )


# --- Book Details Page ---
@app.route('/book_details/<book_title>')
def book_details(book_title):

    the_book = get_book_details(book_title)
    
    if not the_book:
        return "Book not found", 404 
    
    return render_template(
        'book_details.html',
        book=the_book
    )




if __name__ == '__main__':
    app.run(debug=True, port=5000)