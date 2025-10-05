from pymongo import MongoClient
from books import all_books


class Book:
    def __init__(self, genres, title, category, url, description, authors, pages, available, copies):
        self.genres = genres
        self.title = title
        self.category = category
        self.url = url
        self.description = description
        self.authors = authors
        self.pages = pages
        self.available = available
        self.copies = copies

    def to_dict(self):
        return {
            "genres": self.genres,
            "title": self.title,
            "category": self.category,
            "url": self.url,
            "description": self.description,
            "authors": self.authors,
            "pages": self.pages,
            "available": self.available,
            "copies": self.copies
        }
