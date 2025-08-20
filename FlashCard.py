import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

class Card:
    def __init__(self, front, back):
        self.front = front
        self.back = back
    
    def print_card(self):
        print(self.front + " " + self.back)
    

class Deck:
    def __init__(self):
        # create a deck of flash cards from textfile
        self.cards= []
        self.name = ""
        self.numCards = 0

    def add_card(self, front, back):
        self.cards.append(Card(front, back))
        self.numCards += 1
    
    def clear_deck(self):
        self.cards = []
        self.numCards = 0
        self.name = ""

    def rename(self, name: str):
        self.name = name

    # not used
    def rand_sel(self, numCards):
        selected = []
        ranSample = random.sample(self.cards,numCards)
        for card in ranSample:
            selected.append({'front': card.front, 'back': card.back})
        return selected

    def print_front(self):
        for card in self.cards:
            print(card.front)

    def view_deck(self):
        for card in self.cards:
            card.print_card()
