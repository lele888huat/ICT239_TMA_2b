from flask import Flask, session
from flask_mongoengine import MongoEngine
from datetime import timedelta

db = MongoEngine()  # declare globally so it can be imported in models.py later

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    #Remember me settings
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    app.config['REMEMBER_COOKIE_REFRESH_EACH_REQUEST'] = False

    app.config['MONGODB_SETTINGS'] = {
        'db': 'libraryDB',
        'host': 'localhost',
        'port': 27017
    }

    db.init_app(app)  
    return app
