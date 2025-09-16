import pytest
import os
from __init__ import create_app, db
from DeckActions import *
from models import Deck, Card

@pytest.fixture
def app():
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()
        print("Tables created:", table_names)
        yield app
        db.drop_all()
    if os.path.exists('test_flashcards.db'):
        os.remove('test_flashcards.db')

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_deck(app):
    with app.app_context():
        # Test creating a deck
        deck = create_deck("Test Deck")
        assert deck is not None
        assert deck.name == "Test Deck"
        assert deck.id is not None
        
        # Test get by name
        found_deck = get_deck_by_name("Test Deck")
        assert found_deck.name == "Test Deck"