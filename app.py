from flask import Flask, request, jsonify, render_template
from DeckActions import loadDeck, randomCards, rename
from FlashCard import Deck
import json
import os, csv, sys
# TODO: Uploading own Deck, Either that or Availible Decks?
# Uploading own deck, how will it work, will it replace the deck or append it to the current deck?
sys.stdout.reconfigure(encoding='utf-8')
app = Flask(__name__)
deck = Deck()
deck = loadDeck(deck, "Hiragana")

@app.route('/', methods=['POST', 'GET'])
def index():
    # Higher Priority if the upload field is filled!
    # if request.method == "POST" and File exists...
    if request.method== "POST":
        if "file" in request.files:
            file = request.files['file']
            if file.filename:
                print("We have a FILE")
                print(file.filename)
                textfile = file.stream.fileno()
                deck.clearDeck()
                deck.addCards(textfile)
                deck.rename(file.filename)
        if "cardCount" in request.form:
            numCards = request.form.get("cardCount")
            print(numCards)
            cards = randomCards(deck, int(numCards))
            return render_template('index.html', cards = cards, currDeck = deck)
    return render_template("index.html",  currDeck = deck)


if __name__ == '__main__':
    app.run(debug=True)