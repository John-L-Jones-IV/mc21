#!/usr/bin/env python3
from __future__ import annotations
from enum import IntEnum
from enum import auto
import random

# Card types
CARD_VALS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_SUITS = ["hearts", "spades", "clubs", "diamonds"]

class Card:
    def __init__(self, suit, val):
        assert suit in CARD_SUITS
        assert val in CARD_VALS
        self.suit = suit
        self.val = val
        self.showing = False

    def get_num_val(self, hard=False):
        if self.val == "blank":
            raise ValueError("Cannot evaluate card with", self.val, "value.")
        if self.val == "A":
            if hard:
                return 1
            else:
                return 11
        if self.val == "J" or self.val == "Q" or self.val == "K":
            return 10
        return int(self.val)
    
    def set_showing(self, showingState: bool) -> None:
        self.showing = showingState

    def get_suit(self):
        return self.suit

    def get_val(self):
        return self.val


def build_draw_deck(num_decks: int) -> List(Card):
    pile = []
    for _ in range(num_decks):
        for card_val in CARD_VALS:
            for card_suit in CARD_SUITS:
                pile.append(Card(card_suit, card_val))
    random.shuffle(pile)
    return pile


class Player:
    def __init__(self, starting_cash):
        self.hands = [[]]  # list of lists of cards, multiple for split hands.
        self.bank = starting_cash
        self.bet = None

    def add_card_to_hand(self, card):
        card.set_showing(True)
        self.hands[-1].append(card)
    
    def get_hand(self):
        return self.hands[-1]


class Dealer:
    hand = []  # list of cards

    def add_card_to_hand(self, card):
        if len(self.hand) == 1:
            card.set_showing(True)
        self.hand.append(card)

    def get_hand(self):
        return self.hand


class GameState(IntEnum):
    MENU_AND_SETTINGS = auto()
    PLACING_BETS = auto()
    DEALING_CARDS = auto()
    PLAYERS_PLAYING = auto()
    DEALER_PLAYING = auto()
    EVALUATING_RESULTS = auto()
    SETTLING_BETS = auto()
    CLEARING_TABLE = auto()
