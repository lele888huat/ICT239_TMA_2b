from app import db
from app.books import all_books
from flask_mongoengine import Document
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,timedelta
import random

class Book(db.Document):
    """
    MongoEngine model for books in the library.
    """
    genres = db.ListField(db.StringField(), required=True)
    title = db.StringField(required=True)
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
        Returns the Book document (not a dict).
        """
        return cls.objects(title=title).first()


    @classmethod
    def find_by_category(cls, category):
        """
        Retrieve books filtered by category (or all if category='All'), sorted by title.
        """
        if category == "All":
            return cls.get_all_books()
            
        #sorting by title 
        return list(cls.objects(category=category).order_by('title').as_pymongo())

        # --- METHOD 1: Borrow a book ---
    def borrow(self):
        """Decreases available count when a book is borrowed."""
        if self.available <= 0:
            raise ValueError(f"'{self.title}' is currently not available for loan.")
        self.available -= 1
        self.save()

    # --- METHOD 2: Return a book ---
    def return_book(self):
        """Increases available count when a book is returned."""
        if self.available >= self.copies:
            raise ValueError(f"All copies of '{self.title}' are already in the library.")
        self.available += 1
        self.save()
    


# ----------------------------------------------------------------------
# --- NEW USER MODEL (Database Model) ---
# ----------------------------------------------------------------------

class User(UserMixin, Document):
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    is_admin = db.BooleanField(default=False)  # <-- add this field

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Flask-Login needs this to get user by ID
    def get_id(self):
        return str(self.pk)

from datetime import datetime, timedelta
from mongoengine import *

class Loan(db.Document):
    """
    MongoEngine model for a user's loan.
    """
    member = db.ReferenceField(User, required=True)
    book = db.ReferenceField(Book, required=True)
    borrowDate = db.DateTimeField(default=datetime.utcnow)
    dueDate = db.DateTimeField()  # NEW FIELD for VIEWLOAN
    returnDate = db.DateTimeField()
    renewCount = db.IntField(default=0)

    meta = {'collection': 'loans'}

    # ----------------------------
    # CREATE a loan
    # ----------------------------
    @classmethod
    def create_loan(cls, member, book, borrow_date=None):
        """
        Create a loan for the member if there is no active (unreturned) loan for the same book.
        Decrease book.available if loan is successful.
        borrow_date: optional datetime for random borrow date
        """
        if borrow_date is None:
            borrow_date = datetime.utcnow()  

        # Check for existing unreturned loan
        existing_loan = cls.objects(member=member, book=book, returnDate=None).first()
        if existing_loan:
            raise ValueError(f"User {member.name} already has an unreturned loan for '{book.title}'.")

        # Check book availability
        if book.available <= 0:
            raise ValueError(f"'{book.title}' is currently not available for loan.")

        # Decrease available count
        book.available -= 1
        book.save()

        # Set due date 2 weeks after borrow date
        due_date = borrow_date + timedelta(weeks=2)

        # Create new loan
        loan = cls(member=member, book=book, borrowDate=borrow_date, dueDate=due_date)
        loan.save()
        return loan


    # ----------------------------
    # RETRIEVE loans
    # ----------------------------
    @classmethod
    def get_member_loans(cls, member):
        """Retrieve all loans for a given member."""
        return cls.objects(member=member).order_by('-borrowDate')

    @classmethod
    def get_specific_loan(cls, member, book):
        """Retrieve a specific loan (active or returned) for a member and book."""
        return cls.objects(member=member, book=book).first()

    # ----------------------------
    # UPDATE loans
    # ----------------------------
    def renew_loan(self):
        """Renew an active loan by generating a new borrow date 10–20 days after current borrow date."""
        if self.returnDate:
            raise ValueError("Cannot renew a loan that has already been returned.")
        if self.renewCount >= 2:
            raise ValueError("Cannot renew loan more than 2 times.")

        # Generate a random new borrow date (10–20 days after current borrow date, not after today)
        days_after = random.randint(10, 20)
        new_borrow_date = self.borrowDate + timedelta(days=days_after)
        if new_borrow_date > datetime.utcnow():
            new_borrow_date = datetime.utcnow()

        self.borrowDate = new_borrow_date
        self.dueDate = self.borrowDate + timedelta(weeks=2)
        self.renewCount += 1
        self.save()

    def return_loan(self):
        """Return a borrowed book by setting returnDate 10–20 days after borrowDate, capped at today."""
        if self.returnDate:
            raise ValueError("Loan has already been returned.")

        # Generate a random return date (10–20 days after borrow date, not after today)
        days_after = random.randint(10, 20)
        random_return_date = self.borrowDate + timedelta(days=days_after)
        if random_return_date > datetime.utcnow():
            random_return_date = datetime.utcnow()

        self.returnDate = random_return_date
        self.save()

        book = self.book
        if book.available >= book.copies:
            raise ValueError(f"All copies of '{book.title}' are already in the library.")
        book.available += 1
        book.save()

    # ----------------------------
    # DELETE loan
    # ----------------------------
    def delete_loan(self):
        """Delete a loan only if it has been returned."""
        if not self.returnDate:
            raise ValueError("Cannot delete a loan that has not been returned.")
        self.delete()
