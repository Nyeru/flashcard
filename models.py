from datetime import datetime
from __init__ import db

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to cards
    cards = db.relationship('Card', backref='deck', lazy=True, cascade='all, delete-orphan')
    
    @property
    def numCards(self):
        return len(self.cards)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)
    front = db.Column(db.Text, nullable=False)
    back = db.Column(db.Text, nullable=False)