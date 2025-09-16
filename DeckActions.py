from __init__ import db
from models import Card, Deck
import random
import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
From a "," seperated csv
Create deck with name X where X is the file name
create cards front + "," + back
Create tables for cards and deck
- Current Considerations
    - Rewrite using CRUD
    - Card - Deck relationship
        - one to one would make a LOT of redundant entries
        - deck_id should be expanded to include multiple decks.
        - We must check if card exists and append the deck id to the card.
"""
def load_deck(file_source, name: str):
    existing_deck = Deck.query.filter_by(name=name).first()
    if existing_deck:
        raise ValueError(f"Deck with name '{name}' already exists")
    
    deck = Deck(name=name)
    db.session.add(deck)
    db.session.commit()

    try:
        if isinstance(file_source, str):
            with open(file_source, "r", encoding="utf-8") as f:
                lines = f.readlines()
        else: # uploaded file
            content = file_source.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            lines = content.splitlines()
    except FileNotFoundError:
        db.session.delete(deck)  # Clean up the empty deck
        db.session.commit()
        raise ValueError(f"File not found: {file_source}")

    except UnicodeDecodeError:
        db.session.delete(deck)
        db.session.rollback()
        raise ValueError("File must be UTF-8 encoded")
    except IOError as e:

        db.session.delete(deck)
        db.session.rollback()
        raise ValueError(f"Error reading file: {str(e)}")
    try:
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
                new_card = Card(deck_id = deck.id, front = front, back = back)
                db.session.add(new_card)
                cards_loaded += 1
            else:
                print(f"Warning: skipping empty card at line {line_no}")
        if cards_loaded == 0:
            db.session.delete(deck)
            raise ValueError("No valid cards found in file")

        print(f"Successfully loaded {cards_loaded} cards in deck '{name}'")
        db.session.commit()
        return deck
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error reading file: {str(e)}")
    
# CREATE
'''
Use cases:
Custom deck created by user (for specific subdecks/mixed decks/problem sets):
    - Inputs: Name
    - Can add card to deck ID later
    - Instead of making a new csv, can select from existing cards or add in own card with front/back
        - More user friendly? no need to edit csvs to re-upload
'''
def create_deck(name: str, user_id = None) -> Deck:
    original_name = name
    # validation for name 
    counter = 1
    
    # Auto-rename if conflict
    while deck_exists(name):
        counter += 1
        name = f"{original_name} ({counter})"
    
    deck = Deck(name=name)
    db.session.add(deck)
    db.session.commit()
    return deck

def add_card_to_deck(deck_id: int, front: str, back: str) -> Card:
    deck = get_deck_by_id(deck_id)
    if not deck:
        raise ValueError(f"Deck with ID {deck_id} not found")
    
    # Check for duplicates in this deck
    if card_exists_in_deck(deck_id, front, back):
        raise ValueError("Duplicate card already exists in this deck")
    
    # Create the card
    # We can check if card exists (front/back) then get id and add deck id to card
    card = Card(deck_id=deck_id, front=front.strip(), back=back.strip())
    db.session.add(card)
    db.session.commit()
    return card

# READ
def get_deck_by_id(deck_id: int) -> Deck:
    return db.session.get(Deck, deck_id)

def get_deck_by_name(name: str) -> Deck:
    return db.session.execute(
        db.select(Deck).where(Deck.name == name)
    ).scalar_one_or_none()
    
def get_all_decks() -> list[Deck]:
    return db.session.execute(
        db.select(Deck)).scalars().all()

def deck_exists(name: str) -> bool:
    return get_deck_by_name(name) is not None

def get_card_by_id(card_id: int):
    return db.session.get(Card, card_id)

def get_deck_cards(deck_id: int):
    return db.session.execute(
        db.select(Card).where(Card.deck_id == deck_id)
    ).scalars().all()

def card_exists_in_deck(deck_id: int, front: str, back: str) -> bool:
    existing = db.session.execute(
        db.select(Card).where(
            Card.deck_id ==deck_id,
            Card.front == front, 
            Card.back==back)
    ).scalar_one_or_none()
    return existing is not None

# UPDATE
def update_deck_name(deck_id: int, new_name: str) -> Deck:
    pass
def update_card(card_id: int, front: str, back: str) -> Card:
    pass

# DELETE
def delete_deck(deck_id: int) -> bool:
    pass
def delete_card(card_id: int) -> bool:
    pass
def clear_deck_cards(deck_id: int) -> int:
    pass

def random_cards(deck, num_cards: int ):
    if not deck or not deck.cards:
        return []
    all_cards = [
        {
            'id': card.id,
            'front': card.front, 
            'back': card.back,
            'deck_id': card.deck_id
        }
        for card in deck.cards
    ]
    
    # Handle edge cases
    if num_cards <= 0:
        return []
    if num_cards >= len(all_cards):
        return all_cards
    
    # Return random selection
    return random.sample(all_cards, num_cards)

# if imported
if __name__ == 'DeckActions':
    #print(f"{__name__} was imported")
    pass

# if ran directly
if __name__ == '__main__':
    #print("This was ran directly")
    pass