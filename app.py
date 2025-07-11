from flask import Flask, request, jsonify, render_template
from DeckActions import loadDeck, randomCards
import json
# TODO: Uploading own Deck, Either that or Availible Decks?
# Uploading own deck, how will it work, will it replace the deck or append it to the current deck?
app = Flask(__name__)

deck = loadDeck("Hiragana")
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method== "POST":
        numCards = request.form.get("cardCount")
        print(numCards)
        cards = randomCards(deck, int(numCards))
        # Context Dictionary if need to pass many many variables!
        return render_template('index.html', cards = cards, currDeck = deck)
    return render_template("index.html",  currDeck = deck)


if __name__ == '__main__':
    app.run(debug=True)