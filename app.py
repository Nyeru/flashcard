from flask import Flask, request, jsonify, render_template
from DeckActions import loadDeck, randomCards

app = Flask(__name__)

deck = loadDeck("hiragana")
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/cards', methods=['GET'])
def serve_cards():
    num = request.args.get('n', default=5, type=int)
    cards = randomCards(deck, num)
    print("Working")
    return jsonify(cards)

if __name__ == '__main__':
    app.run(debug=True)