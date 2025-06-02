import csv
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

    def addCards(self,textfile):
        readfile = open(textfile, "r", encoding = 'utf-8')
        for line in readfile:
            rawtext = line.split("\n")
            text = rawtext[0].split(',')
            text[1] = text[1].lstrip()
            self.cards.append(Card(text[0],text[1]))
    
    def clearDeck(self):
        self.cards = []

    def randSel(self):
        selection = random.choice(self.cards)
        front = selection.front
        back = selection.back
        return [front,back]

    def printFront(self):
        for card in self.cards:
            print(card.front)

    def viewDeck(self):
        for card in self.cards:
            card.printCard()
