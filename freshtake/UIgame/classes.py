#!/usr/bin/env python3
from __future__ import annotations
from enum import IntEnum, auto
import random


CARD_VALS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_SUITS = ["hearts", "spades", "clubs", "diamonds"]


class Card:
    def __init__(self, suit, value):
        assert suit in CARD_SUITS
        assert value in CARD_VALS
        self.suit = suit
        self.value = value
        self.showing = False

    def get_value(self, hard=False):
        if self.value == "blank":
            raise ValueError("Cannot evaluate card with", self.value, "value.")
        if self.value == "A":
            if hard:
                return 1
            else:
                return 11
        if self.value == "J" or self.value == "Q" or self.value == "K":
            return 10
        return int(self.value)

    def get_value_as_str(self):
        return self.value

    def set_showing(self, showingState: bool) -> None:
        self.showing = showingState

    def get_suit(self):
        return self.suit

    def __str__(self):
        if self.val == "Blank":
            return "BLANK CARD"
        if self.suit == "Clubs":
            str_suit = "♣"
        elif self.suit == "Heart":
            str_suit = "♥"
        elif self.suit == "Diamond":
            str_suit = "♦"
        elif self.suit == "Spades":
            str_suit = "♠"
        return str(self.val) + " " + str_suit


class Deck:
    def __init__(self, num_decks: int):
        self.num_decks = num_decks
        self.deck = []
        for _ in range(num_decks):
            for card_val in CARD_VALS:
                for card_suit in CARD_SUITS:
                    self.deck.append(Card(card_suit, card_val))
        #    random.shuffle(self.deck)

    def pop(self):
        return self.deck.pop()

    def deal_cards(self, players):
        for _ in range(2):
            for player in players:
                player.add_card_to_hand(self.pop())

    def hit(self, player):
        player.add_card_to_hand(self.deck.pop())


def _soft_hand_value(cards):
    return sum([card.get_value(hard=False) for card in cards])


def _hard_hand_value(cards):
    return sum([card.get_value(hard=True) for card in cards])


def _best_hand_value(cards):
    return (
        _hard_hand_value(cards)
        if _hard_hand_value(cards) <= 21
        else _soft_hand_value(cards)
    )


class Player:
    def __init__(self, starting_cash):
        self.hands = [[]]  # list of lists of cards
        self.bankroll = starting_cash
        self.active_hand = 0  # used to index hands: list(list(Card))

    def split_hand(self):
        self.hands.insert(self.active_hand, [self.hands[self.active_hand].pop()])
        self.active_hand += 1

    def add_card_to_hand(self, card, hand=None):
        if hand is None:
            hand = self.active_hand
        card.set_showing(True)
        self.hands[hand].append(card)

    def get_hand(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return self.hands[hand_idx]

    def get_hand_value(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return _best_hand_value(self.get_hand(hand_idx))

    def get_soft_hand_value(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return _soft_hand_value(self.get_hand(hand_idx))

    def get_hard_hand_value(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return _hard_hand_value(self.get_hand(hand_idx))

    def get_hands(self):
        return self.hands

    def set_wager(self, wager):
        if type(wager) is not int or wager < 0:
            raise ValueError("wager must be an int greater than 0")
        self.wager = wager

    def is_hand_blackjack(self):
        if self.get_hand_value() == 21 and len(self.get_hand()) == 2:
            return True

    def is_hand_bust(self):
        return _best_hand_value(self.get_hand()) > 21


class Dealer:
    hand = []  # list of cards

    def add_card_to_hand(self, card):
        if len(self.hand) == 1:
            card.set_showing(True)
        self.hand.append(card)

    def get_hand(self):
        return self.hand

    def get_card_showing(self):
        return self.hand[1]


class GameState(IntEnum):
    MENU_AND_SETTINGS = auto()
    PLACE_BETS = auto()
    DEAL_CARDS = auto()
    PLAY = auto()
    EVALUATE_RESULTS = auto()
