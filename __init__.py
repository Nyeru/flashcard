from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory for speed
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    return app
