import random

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["C", "D", "H", "S"]
FACES = {"J", "Q", "K"}


class Deck:
    def __init__(self):
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None


def card_name(card):
    rank, suit = card
    return f"{rank}{suit}"


def hand_text(hand):
    return " ".join(card_name(card) for card in hand)


def hand_value(hand):
    """Best total for the hand.

    Every Ace is first counted as 11, then demoted to 1 one at a time for as
    long as the hand is over 21.  A+9 is 20, A+9+5 is 15, A+A+9 is 21.
    """
    value = 0
    aces = 0
    for rank, _ in hand:
        if rank == "A":
            aces += 1
            value += 11
        elif rank in FACES:
            value += 10
        else:
            value += int(rank)
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value


def is_soft(hand):
    """True when an Ace in the hand is still being counted as 11."""
    hard = sum(1 if rank == "A" else 10 if rank in FACES else int(rank)
               for rank, _ in hand)
    return hand_value(hand) != hard


def is_blackjack(hand):
    """A natural: exactly two cards totalling 21."""
    return len(hand) == 2 and hand_value(hand) == 21
