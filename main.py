from FlashCard import Deck

Deck1 = Deck()
csvName = "Hiragana"
Deck1.addCards(csvName+".csv")
print(f"{csvName} Deck Loaded.\n")
numCards = "a"
while numCards.isnumeric() is False:
    numCards = input(f"Enter the amount of cards from {csvName} Deck to practice with:")
    if numCards.isnumeric() is False:
        print("Please input a number.")

for i in range (int(numCards)):
    [front,back] = Deck1.randSel()
    print("Press Enter to reveal the back")
    print(front, end='')
    input("")
    print(back)