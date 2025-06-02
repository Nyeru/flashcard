from FlashCard import Deck

Deck1 = Deck()
Deck1.addCards("Hiragana.csv")
# Deck1.viewDeck()
for i in range (5):
    [front,back] = Deck1.randSel()
    print(front)
    input("Press Enter to reveal the back")
    print(front, back)