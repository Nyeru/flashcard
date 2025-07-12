from FlashCard import Deck
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

def emptyDeck(deck:Deck):
    deck.clearDeck()
    return deck

def loadDeck(deck: Deck, fileStream, name: str):
    deck.clearDeck()
    readfile = open(fileStream, "r", encoding = 'utf-8')
    for line in readfile:
        rawtext = line.split("\n")
        text = rawtext[0].split(',')
        text[1] = text[1].lstrip()
        deck.addCard(text[0], text[1])
    deck.rename(name)
    return deck


def randomCards(deck: Deck, numCards: int ):
    return deck.randSel(numCards)

def randomCardsCLI(deck: Deck, numCards: int):
    for _ in range(numCards):
        front, back = deck.randSel()
        input(f"{front} — press enter to reveal")
        print(f"{back}\n")


def rename(deck: Deck, name: str):
    deck.name = name

# if imported
if __name__ == 'DeckActions':
    #print(f"{__name__} was imported")
    pass

# if ran directly
if __name__ == '__main__':
    #print("This was ran directly")
    pass