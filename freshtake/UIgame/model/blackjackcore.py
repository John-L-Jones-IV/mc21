#!/usr/bin/env python3
from __future__ import annotations
from enum import IntEnum, auto
import copy
import random

# inital game settings, can be changed
NUM_DECKS_IN_GAME = 6
STARTING_CASH = 200
MIN_BET = 5
MAX_SPLITS = 4
BLACKJACK_PAYS = 3.0/2.0

# generally, don't touch these.
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
    def __init__(self, bet=None):
        self.hand = []  # List of Card
        self.bet = bet

    def __iter__(self):
        return self.hand.__iter__()
    
    def __next__(self):
        return self.hand.__next__()
    
    def __len__(self):
        return self.hand.__len__()

    def __getitem__(self, key: int) -> Card:
        return self.hand[key]
    
    def set_bet(self, wager):
        self.wager = wager

    def get_bet(self):
        return self.wager

    def pop(self):
        return self.hand.pop()

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
        best_hand_value = self.get_best_value()
        aces_used_in_best_hand = (max_hand_value - best_hand_value) // 10
        num_aces = self._get_num_aces()
        for ace_cnt in range(aces_used_in_best_hand + 1, num_aces + 1):
            if max_hand_value - (ace_cnt * 10) <= 21:
                return max_hand_value - (ace_cnt * 10)
        return max_hand_value - (num_aces * 10)

    def is_bust(self):
        return self.get_best_value() > 21
    
    def is_blackjack(self):
        return (self.get_best_value() == 21 and len(self.hand) ==2)


class Deck:
    def __init__(self, num_decks: int):
        self.num_decks = num_decks
        self.deck = []
        for _ in range(num_decks):
            for card_val in CARD_VALS:
                for card_suit in CARD_SUITS:
                    self.deck.append(Card(card_suit, card_val))
        #    random.shuffle(self.deck)

    def __len__(self):
        return self.deck.__len__()
    
    def __iter__(self):
        return self.deck.__iter__()

    def __next__(self):
        return self.deck.__next__()

    def pop(self):
        if len(self.deck) == 0:
            raise Exception("can not pop() from empty Deck")
        return self.deck.pop()

    def deal_cards(self, players):
        for _ in range(2):
            for player in players:
                player.add_card_to_hand(self.pop())

    def hit(self, player):
        player.add_card_to_hand(self.deck.pop())

    def append(self, card: Card()):
        self.deck.append(card)


class Player:
    def __init__(self, bankroll=STARTING_CASH):
        self.hands = [Hand()]   # list of Hand to handle splits
        self.active_hand_index = 0
        self.bankroll = bankroll

    def get_bankroll(self):
        return self.bankroll

    def add_to_bankroll(self, dollar_amount):
        self.bankroll += dollar_amount

    def get_active_hand_index(self):
        return self.active_hand_index

    def get_hand(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand_index
        return self.hands[hand_idx]

    def get_hands(self):
        return self.hands

    def get_best_hand_value(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand_index
        return self.hands[hand_idx].get_best_value()

    def get_second_best_hand_value(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand_index
        return self.hands[hand_idx].get_second_best_value()

    def set_wager(self, wager):
        if type(wager) is not int or wager < 0:
            raise ValueError("Wager must be an int greater than 0")
        self.wager = wager

    def is_hand_blackjack(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand_index
        return self.hands[hand_idx].is_blackjack()

    def is_hand_bust(self, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand_index
        return self.hands[hand_idx].is_bust()

    def split_hand(self):
        hand_idx = self.active_hand_index
        new_hand = Hand()
        new_hand.add_card(self.get_hand().pop())
        self.hands.insert(hand_idx, new_hand)
        self.active_hand_index += 1

    def add_card_to_hand(self, card, hand_idx=None):
        if hand_idx is None:
            hand_idx = self.active_hand_index
        card.set_showing(True)
        self.hands[hand_idx].add_card(card)

    def move_all_cards(self, destination: Deck()):
        assert isinstance(destination, Deck)
        copy_hands = copy.deepcopy(self.hands)
        for hand_cnt, copy_hand in enumerate(copy_hands):
            for copy_card in copy_hand:
                copy_card.set_showing(False)
                destination.append(copy_card)
                self.hands[hand_cnt].pop()


class Dealer:
    def __init__(self):
        self.hand = Hand()

    def add_card_to_hand(self, card):
        if len(self.hand) == 1:
            card.set_showing(True)
        self.hand.add_card(card)

    def get_hand(self):
        return self.hand

    def get_card_showing(self):
        return self.hand[1]

    def move_all_cards(self, destination: list()):
        copy_hand = copy.deepcopy(self.hand)
        for i, copy_card in enumerate(copy_hand):
            copy_card.set_showing(False)
            destination.append(copy_card)
            self.hand.pop()


class GameState(IntEnum):
    MENU_AND_SETTINGS = auto()
    PLACE_BETS = auto()
    DEAL_CARDS = auto()
    PLAY = auto()
    EVALUATE_RESULTS = auto()


class Game:
    def __init__(self):
        self.deck = Deck(NUM_DECKS_IN_GAME)
        self.discard_pile = Deck(0)
        self.player1 = Player(STARTING_CASH)
        self.dealer = Dealer()
        self.state = GameState.DEAL_CARDS
        self.players = [player1] # list for expandability
        self.active_player_index = 0
        self.players_and_dealer = players + [dealer]

    def get_state(self) -> GameState:
        return self.state
    
    def clear_table(self):
        for player in self.players_and_dealer:
            player.move_all_cards(self.discard_pile)

    def evaluate_hands(self):
        dealer_score = self.dealer.get_hand().get_best_value_as_int()

        for player in self.players:
            for hand in player.get_hands():
                if hand.is_blackjack() and not dealer.hand.is_blackjack():
                    winnings = hand.get_bet() * BLACKJACK_PAYS
                    player.add_to_bankroll(winnings)
                elif hand.is_bust():
                    losses = -1 * hand.get_bet()
                    player.add_to_bankroll(losses)
                elif hand.get_value_as_int() > dealer_score:
                    winnings = hand.get_bet()
                    player.add_to_bankroll(winnings)
                elif hand.get_value_as_int() < dealer_score:
                    losses = -1 * hand.get_bet()
                    player.add_to_bankroll(losses)
                else:
                    pass # push, no money won, no money lost
