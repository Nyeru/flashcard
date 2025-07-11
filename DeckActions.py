from FlashCard import Deck
import random

def loadDeck(name: str):
    loadedDeck = Deck()
    loadedDeck.addCards(name+".csv")
    print(f"{name} Deck Loaded.\n")
    return loadedDeck

def randomCards(deck: Deck, numCards: int ):
    return deck.randSel(numCards)

def randomCardsCLI(deck: Deck, numCards: int):
    for _ in range(numCards):
        front, back = deck.randSel()
        input(f"{front} — press enter to reveal")
        print(f"{back}\n")
    
# if imported
if __name__ == 'DeckActions':
    #print(f"{__name__} was imported")
    pass

# if ran directly
if __name__ == '__main__':
    #print("This was ran directly")
    pass