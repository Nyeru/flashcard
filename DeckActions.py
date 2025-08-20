from FlashCard import Deck
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

def empty_deck(deck:Deck):
    deck.clear_deck()
    return deck

def load_deck(deck: Deck, file_source, name: str):
    deck.clear_deck()
    try:
        if isinstance(file_source, str):
            with open(file_source, "r", encoding="utf-8") as f:
                lines = f.readlines()
        else: # uploaded file
            content = file_source.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            lines = content.splitlines()
        cards_loaded = 0
        for line_no, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split(',', 1)
            if len(parts) != 2:
                print(f"Warning: Skipping malformed line {line_no}: '{line}'")
                continue

            front = parts[0].strip()
            back = parts[1].strip()

            if front and back:
                deck.add_card(front, back)
                cards_loaded += 1
            else:
                print(f"Warning: skipping empty card at line {line_no}")
        if cards_loaded == 0:
            raise ValueError("No valid cards found in file")

        deck.rename(name)
        print(f"Successfully loaded {cards_loaded} cards in deck '{name}'")
        return deck
    except UnicodeDecodeError:
        deck.clear_deck()
        raise ValueError("File must be UTF-8 encoded")
    except IOError as e:
        deck.clear_deck()
        raise ValueError(f"Error reading file: {str(e)}")
    except Exception as e:
        deck.clear_deck()
        raise ValueError(f"Error reading file: {str(e)}")
    
def random_cards(deck: Deck, num_cards: int ):
    return deck.rand_sel(num_cards)

def random_cards_cli(deck: Deck, num_cards: int):
    for _ in range(num_cards):
        cards = deck.rand_sel(1)  # Get one random card
        front, back = cards[0]['front'], cards[0]['back']  # Extract from dictionary
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