from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()  # declare globally so it can be imported in models.py later

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'libraryDB',
        'host': 'localhost',
        'port': 27017
    }

    db.init_app(app)  
    return app
