from flask import Flask, request, jsonify, render_template, flash
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
            num_cards = request.form.get("card_count")
            print(num_cards)
            cards = random_cards(deck, int(num_cards))
            return render_template('deck.html', cards = cards, curr_deck = deck)
    return render_template("index.html",  curr_deck = deck)

@app.route('/CardList/')
def viewDeck():
    print(deck.name)
    return render_template("deck.html", curr_deck = deck)

if __name__ == '__main__':
    app.run(debug=True)