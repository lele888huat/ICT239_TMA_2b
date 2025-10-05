
from flask import Flask, render_template, request
from app import create_app, db 
from app.model import Book

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


if __name__ == '__main__':
    app.run(debug=True, port=5000)