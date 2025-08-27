from flask import Flask, request, jsonify, render_template, flash, session, redirect, url_for
from DeckActions import *
from FlashCard import Deck
import json
import os, csv, sys
import secrets
# TODO: Uploading own Deck, Either that or Availible Decks?
# Uploading own deck, how will it work, will it replace the deck or append it to the current deck?
sys.stdout.reconfigure(encoding='utf-8')
app = Flask(__name__)
deck = Deck()
app.secret_key = secrets.token_hex(16)
deck = load_deck(deck, "Hiragana.csv", "Hiragana")

@app.route('/', methods=['POST', 'GET'])
def index():
    # Higher Priority if the upload field is filled!
    # if request.method == "POST" and File exists...
    if request.method== "POST":
        if "file" in request.files:
            file = request.files['file']
            if file.filename:
                try:
                    print(f"Processing uploaded file: {file.filename}")
                    if not file.filename.lower().endswith('.csv'):
                        flash("Please upload a CSV file", "error")
                        return render_template("index.html", curr_deck=deck)
                    deck_name = os.path.splitext(file.filename)[0]
                    load_deck(deck, file.stream, deck_name)
                    flash(f"Successfully loaded deck '{deck_name}' with {deck.numCards} cards", "success")
                except ValueError as e:
                    flash(f"Error loading file: {str(e)}", "error")
                except Exception as e:
                    flash(f"Unexpected error: {str(e)}", "error")

        if "card_count" in request.form:
            try:
                num_cards = int(request.form.get("card_count"))
                
                if num_cards < 1 :
                    flash("Please select at least 1 card", "error")
                    return redirect(url_for('index'))
                elif num_cards > deck.numCards:
                    flash(f"Cannot select more than {deck.numCards} cards", "error")
                    return redirect(url_for('index'))
                cards = random_cards(deck, int(num_cards))
                session['study_cards'] = cards
                session['current_card'] = 0
                return redirect(url_for('study'))
            except(ValueError, TypeError):
                flash("Please enter a valid number", "error")
                return render_template("index.html", curr_deck = deck)
    return render_template("index.html",  curr_deck = deck)

@app.route('/study', methods =['GET', 'POST'])
def study():
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
                    'deck_name': deck.name
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
                         deck_name=deck.name)

@app.route('/CardList/',  methods=['POST', 'GET'])
def viewDeck():
    print(deck.name)
    if request.method== "POST":
        num_cards = request.form.get("card_count")
        cards = random_cards(deck, int(num_cards))
        session['study_cards'] = cards
        session['current_card'] = 0
        return redirect(url_for('study',
                                total_cards = len(cards),
                                current_card = 0,
                                card = cards[0],
                                deck_name = deck.name))
    return render_template("deck.html", curr_deck = deck)

@app.route('/study-complete')
def study_complete():
    completion_data = session.pop('completion_data', None)
    if not completion_data:
        return redirect(url_for('index'))
    return render_template('study_complete.html', **completion_data)
if __name__ == '__main__':
    app.run(debug=True)