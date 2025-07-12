import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

class Card:
    def __init__(self, front, back):
        self.front = front
        self.back = back
    
    def printCard(self):
        print(self.front + " " + self.back)
    

class Deck:
    def __init__(self):
        # create a deck of flash cards from textfile
        self.cards= []
        self.name = ""
        self.numCards = 0

    def addCards(self,textfile):
        readfile = open(textfile, "r", encoding = 'utf-8')
        for line in readfile:
            rawtext = line.split("\n")
            text = rawtext[0].split(',')
            text[1] = text[1].lstrip()
            self.cards.append(Card(text[0],text[1]))
        self.name = textfile
        self.numCards = len(self.cards)
        readfile.close()
    
    def clearDeck(self):
        self.cards = []
        self.numCards = 0
        self.name = ""

    def rename(self, name: str):
        self.name = name

    # not used
    def randSel(self, numCards):
        selected = []
        ranSample = random.sample(self.cards,numCards)
        for card in ranSample:
            selected.append({'front': card.front, 'back': card.back})
        return selected

    def printFront(self):
        for card in self.cards:
            print(card.front)

    def viewDeck(self):
        for card in self.cards:
            card.printCard()
