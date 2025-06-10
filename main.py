from FlashCard import Deck
import DeckActions

def main():
    cardList = 'hiragana'
    Deck1 = DeckActions.loadDeck(cardList)
    numCards = "a"
    while numCards.isnumeric() is False:
        numCards = input(f"Enter the amount of cards from {cardList} Deck to practice with:")
        if numCards.isnumeric() is False:
            print("Please input a number.")

    DeckActions.randomCards(Deck1, numCards)
    # TODO: read https://realpython.com/python-main-function/


if __name__ == '__main__':
    main()