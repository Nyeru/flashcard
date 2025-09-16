from flask import Flask, request, jsonify, render_template, flash, session, redirect, url_for
from DeckActions import *
import json
import os, csv, sys
import secrets
from flask_sqlalchemy import SQLAlchemy
from models import Deck, Card
from __init__ import create_app, db

sys.stdout.reconfigure(encoding='utf-8')

app = create_app()
with app.app_context():
    db.create_all()
app.secret_key = secrets.token_hex(16)

def get_current_deck():
    deck_id = session.get('current_deck_id')
    if deck_id:
        return db.session.get(Deck, deck_id) 
    
    # Fallback to first available deck
    first_deck = Deck.query.first()
    if first_deck:
        session['current_deck_id'] = first_deck.id
        return first_deck
    
    return None

def create_test_deck():
    """Create a simple test deck if none exist"""
    if Deck.query.count() == 0:
        test_deck = Deck(name="Test Hiragana")
        db.session.add(test_deck)
        db.session.commit()
        
        # Add a few test cards
        test_cards = [("あ", "a"), ("い", "i"), ("う", "u")]
        for front, back in test_cards:
            card = Card(deck_id=test_deck.id, front=front, back=back)
            db.session.add(card)
        db.session.commit()
        print(f"Created test deck with {len(test_cards)} cards")

# Call after db.create_all()
with app.app_context():
    db.create_all()
    create_test_deck()
    

@app.route('/', methods=['POST', 'GET'])
def index():
    all_decks = Deck.query.all()
    selected_deck_id = session.get('current_deck_id')
    current_deck = None
    if selected_deck_id:
        
        current_deck = db.session.get(Deck, selected_deck_id) 
    
    if not current_deck and all_decks:
        current_deck = all_decks[0]  # Default to first deck
        session['current_deck_id'] = current_deck.id
    
    if request.method== "POST":
        
        if "file" in request.files:
            file = request.files['file']
            if file.filename:
                try:
                    print(f"Processing uploaded file: {file.filename}")
                    if not file.filename.lower().endswith('.csv'):
                        flash("Please upload a CSV file", "error")
                        return render_template("index.html", curr_deck=current_deck)
                    deck_name = os.path.splitext(file.filename)[0]
                    current_deck = load_deck(file.stream, deck_name)
                    flash(f"Successfully loaded deck '{deck_name}' with {current_deck.numCards} cards", "success")
                    return redirect(url_for('index'))
                except ValueError as e:
                    flash(f"Error loading file: {str(e)}", "error")
                except Exception as e:
                    flash(f"Unexpected error: {str(e)}", "error")

    if not current_deck:
        class EmptyDeck:
            name = "No Decks Available"
            numCards = 0
        current_deck = EmptyDeck()

    if "card_count" in request.form:
            try:
                num_cards = int(request.form.get("card_count"))
                if num_cards < 1 :
                    flash("Please select at least 1 card", "error")
                    return redirect(url_for('index'))
                elif num_cards > current_deck.numCards:
                    flash(f"Cannot select more than {current_deck.numCards} cards", "error")
                    return redirect(url_for('index'))
                cards = random_cards(current_deck, int(num_cards))
                session['study_cards'] = cards
                session['current_card'] = 0
                return redirect(url_for('study'))
            except(ValueError, TypeError):
                flash("Please enter a valid number", "error")
                return render_template("index.html", curr_deck = current_deck, all_decks= all_decks)
    
    return render_template("index.html",  curr_deck = current_deck, all_decks = all_decks)

@app.route('/select-deck', methods=['POST'])
def select_deck():
    deck_id = request.form.get('deck_id')
    if deck_id:
        session['current_deck_id'] = int(deck_id)
        flash(f"Switched to deck", "success")
    return redirect(url_for('index'))

@app.route('/CardList/',  methods=['POST', 'GET'])
def viewDeck():
    current_deck = get_current_deck()
    if not current_deck:
        flash("No deck found", "error")
        return redirect(url_for('index'))
    print(current_deck.name)

    if request.method== "POST":
        pass
    return render_template("deck.html", curr_deck = current_deck)

@app.route('/study', methods =['GET', 'POST'])
def study():    
    current_deck = get_current_deck()
    if not current_deck:
        flash("No deck found", "error")
        return redirect(url_for('index'))
    
    study_cards = session.get('study_cards', [])
    curr_index = session.get('current_card', 0)
    if not study_cards:
        flash("No study session active. Please select cards to study.", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'next' and curr_index < len(study_cards) - 1:
            session['current_card'] = curr_index + 1
        elif action == 'previous' and curr_index > 0:
            session['current_card'] = curr_index - 1
        elif action == 'finish':
            session.pop('study_cards', None)
            session.pop('current_card', None)
            session['completion_data'] = {
                    'total_studied': len(study_cards),
                    'deck_name': current_deck.name
                }
            return redirect(url_for('study_complete'))
        curr_index = session.get('current_card', 0)

    current_card = study_cards[curr_index]
    progress_percent = ((curr_index + 1) / len(study_cards)) * 100
    return render_template('study.html',
                         card=current_card,
                         current_card=curr_index,
                         total_cards=len(study_cards),
                         progress = progress_percent,
                         deck_name=current_deck.name)

@app.route('/study-complete')
def study_complete():
    completion_data = session.pop('completion_data', None)
    if not completion_data:
        return redirect(url_for('index'))
    return render_template('study_complete.html', **completion_data)

if __name__ == '__main__':
    app.run(debug=True)