from app import db
from app.books import all_books

class Book(db.Document):
    """
    MongoEngine model for books in the library.
    """
    genres = db.ListField(db.StringField(), required=True)
    title = db.StringField(required=True, unique=True)
    category = db.StringField(required=True)
    url = db.StringField()
    description = db.ListField(db.StringField()) 
    authors = db.ListField(db.StringField(), required=True)
    pages = db.IntField()
    available = db.IntField(default=0) 
    copies = db.IntField(default=0)

    meta = {'collection': 'books'}

    # --- Class Methods ---
    @classmethod
    def initialize_collection(cls):
        """
        Populate the collection from all_books if empty.
        """
        if cls.objects.count() == 0:
            print("Book collection is empty. Initializing from all_books...")
            for book_data in all_books:
                # The data structure in books.py already matches the model,
                # except for the default values which MongoEngine handles.
                cls(**book_data).save()
            print(f"✅ Book collection initialized from all_books.")
        else:
            print(f"ℹ️ Book collection already populated with {cls.objects.count()} documents. Skipping initialization.")


    @classmethod
    def get_all_books(cls):
        """
        Retrieve all books from MongoDB, sorted by title (Required for Q2(a) effect).
        """
        # --- CORRECTION 3: Added sorting by title ---
        return list(cls.objects.order_by('title').as_pymongo())

    @classmethod
    def find_by_title(cls, title):
        """
        Find a single book by title.
        """
        book = cls.objects(title=title).first()
        return book.to_mongo().to_dict() if book else None

    @classmethod
    def find_by_category(cls, category):
        """
        Retrieve books filtered by category (or all if category='All'), sorted by title.
        """
        if category == "All":
            return cls.get_all_books()
            
        #sorting by title 
        return list(cls.objects(category=category).order_by('title').as_pymongo())
    


# ----------------------------------------------------------------------
# --- NEW USER MODEL (Database Model) ---
# ----------------------------------------------------------------------
class User(db.Document):
    """
    MongoEngine model for users (librarians/members).
    """
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True) 
    name = db.StringField(required=True)

    meta = {'collection': 'users'}

