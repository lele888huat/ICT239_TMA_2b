from app import db
from books import all_books

class Book(db.Document):
    """
    MongoEngine model for books in the library.
    """
    genres = db.ListField(db.StringField(), required=True)
    title = db.StringField(required=True, unique=True)
    category = db.StringField(required=True)
    url = db.StringField()
    description = db.StringField()
    authors = db.ListField(db.StringField(), required=True)
    pages = db.IntField()
    available = db.BooleanField(default=True)
    copies = db.IntField(default=1)

    meta = {'collection': 'books'}  # optional, sets the MongoDB collection name

    # --- Class Methods ---
    @classmethod
    def initialize_collection(cls):
        """
        Populate the collection from all_books if empty.
        """
        if cls.objects.count() == 0:
            for book_data in all_books:
                cls(**book_data).save()
            print("✅ Book collection initialized from all_books.")
        else:
            print("ℹ️ Book collection already populated.")

    @classmethod
    def get_all_books(cls):
        """
        Retrieve all books from MongoDB.
        """
        return list(cls.objects.as_pymongo())

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
        Retrieve books filtered by category (or all if category='All').
        """
        if category == "All":
            return cls.get_all_books()
        return list(cls.objects(category=category).as_pymongo())
