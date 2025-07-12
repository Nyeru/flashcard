from FlashCard import Deck
import DeckActions
from flask import Flask, jsonify, request

def main():
    cardList = 'hiragana.csv'
    Deck1 = DeckActions.loadDeck(cardList)
    numCards = -1
    
    numCards = getInt(f"Enter the amount of cards from {cardList} Deck to practice with:")
    selected = DeckActions.randomCardsCLI(Deck1, numCards)

    # TODO: read https://realpython.com/python-main-function/
10
def getInt(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Please input a number.")
            
if __name__ == '__main__':
    main()