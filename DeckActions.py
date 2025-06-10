from FlashCard import Deck

def loadDeck(name: str):
    loadedDeck = Deck()
    loadedDeck.addCards(name+".csv")
    print(f"{name} Deck Loaded.\n")
    return loadedDeck

def randomCards(deck: Deck, numCards: int ):
    for i in range (int(numCards)):
        [front,back] = deck.randSel()
        print("Press Enter to reveal the back")
        print(front, end='')
        input("")
        print(back)

# if imported
if __name__ == 'DeckActions':
    #print(f"{__name__} was imported")
    pass

# if ran directly
if __name__ == '__main__':
    #print("This was ran directly")
    pass