from flask import Flask, request, jsonify, render_template
from DeckActions import loadDeck, randomCards
import json
# TODO: List of availibe CSV, Dynamic Loading, Refreshing Gives new cards, Dynamic Number of Cards

app = Flask(__name__)

deck = loadDeck("Hiragana")
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method== "POST":
        numCards = request.form.get("cardCount")
        print(numCards)
        cards = randomCards(deck, int(numCards))
        return render_template('index.html', cards = cards)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)