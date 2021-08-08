#!/usr/bin/env python3
from __future__ import annotations
from enum import IntEnum, auto
import copy
import random


CARD_VALS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_SUITS = ["hearts", "spades", "clubs", "diamonds"]


class Card:
    # TODO: change parameters to value, suit
    def __init__(self, suit: str, value: str):
        assert suit in CARD_SUITS
        assert value in CARD_VALS
        self.suit = suit
        self.value = value
        self.showing = False

    def get_value_as_int(self, hard=False) -> int:
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

    def get_value_as_str(self) -> str:
        return self.value

    def set_showing(self, showingState: bool) -> None:
        self.showing = showingState

    def get_suit(self) -> str:
        return self.suit

    def __str__(self):
        if self.value == "Blank":
            return "BLANK CARD"
        elif self.suit == "clubs":
            str_suit = "♣"
        elif self.suit == "heart":
            str_suit = "♥"
        elif self.suit == "diamonds":
            str_suit = "♦"
        elif self.suit == "spades":
            str_suit = "♠"
        return str(self.value) + " " + str_suit

class Hand:
    def __init__(self):
        self.hand = []  # List of Card

    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise TypeError("card must be of type Card")
        self.hand.append(card)

    def _get_num_aces(self):
        num_aces = 0
        for card in self.hand:
            if card.get_value_as_str() == "A":
                num_aces += 1
        return num_aces
    
    def get_best_value(self):
        max_hand_value = sum(card.get_value_as_int() for card in self.hand)
        if max_hand_value <= 21:
            return max_hand_value
        for num_aces in range(0, self._get_num_aces() + 1):
            if max_hand_value - (num_aces * 10) <= 21:
                return max_hand_value - (num_aces * 10)
        return max_hand_value - (num_aces * 10)

    def get_second_best_value(self):
        max_hand_value = sum(card.get_value_as_int() for card in self.hand)
        best_hand_value = self.get_best_hand_value()
        aces_used_in_best_hand = (max_hand_value - best_hand_value) // 10
        num_aces = self._get_num_aces()
        for ace_cnt in range(aces_used_in_best_hand + 1, num_aces + 1):
            if max_hand_value - (act_cnt * 10) <= 21:
                return max_hand_value - (act_cnt * 10)
        return max_hand_value - (act_cnt * 10)

    def is_bust(self):
        return self.get_best_hand_value() > 21
    
    def is_black_jack(self):
        return (self.get_best_hand_value() == 21 and len(self.hand) ==2)


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

    def append(self, card: Card()):
        self.deck.append(card)




class Hand:
    def __init__(self):
        pass # TODO:


class Player:
    def __init__(self, starting_cash):
        self.hands = [[]]  # list of lists of cards
        self.bankroll = starting_cash
        self.active_hand = 0  # used to index hands: list(list(Card))

    def split_hand(self):
        self.hands.insert(self.active_hand,
                          [self.hands[self.active_hand].pop()])
        self.active_hand += 1

    def get_active_hand(self):
        return self.active_hand

    def add_card_to_hand(self, card, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        card.set_showing(True)
        self.hands[hand_idx].append(card)

    def get_hand(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return self.hands[hand_idx]

    def get_hand_value(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return _best_hand_value(self.get_hand(hand_idx))

    # FIXME: replace with best hand value
    def get_soft_hand_value(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return _soft_hand_value(self.get_hand(hand_idx))

    # FIXME: replace with second best hand value
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

    def is_hand_blackjack(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return (self.get_hand_value(hand_idx) == 21 
                and len(self.get_hand(hand_idx)) == 2)

    def is_hand_bust(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand
        return _best_hand_value(self.get_hand(hand_idx)) > 21
    
    def move_all_cards(self, destination: list()):
        hands = copy.deepcopy(self.hands)
        for hand_cnt, hand in enumerate(hands):
            for card in hand:
                destination.append(self.hands[hand_cnt].pop())

    
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

    def move_all_cards(self, destination: list()):
        hand = copy.deepcopy(self.hand)
        print(f'len dealer hand: {len(hand)}')
        for i, card in enumerate(hand):
            print(f"dealer card #: {i}")
            destination.append(self.hand.pop())


class GameState(IntEnum):
    MENU_AND_SETTINGS = auto()
    PLACE_BETS = auto()
    DEAL_CARDS = auto()
    PLAY = auto()
    EVALUATE_RESULTS = auto()
