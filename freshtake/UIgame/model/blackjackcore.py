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
BLACKJACK_PAYS = 3.0 / 2.0

# generally, don't touch these.
CARD_VALS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_SUITS = ["hearts", "spades", "clubs", "diamonds"]


class GameState(IntEnum):
    MENU_AND_SETTINGS = auto()
    PLACE_BETS = auto()
    DEAL_CARDS = auto()
    PLAY = auto()
    EVALUATE_RESULTS = auto()


class Card:
    def __init__(self, suit: str, value: str):
        assert suit in CARD_SUITS
        assert value in CARD_VALS
        self.suit = suit
        self.value = value
        self.showing = False

    @property
    def int_value(self):
        """get the interger value of a card"""
        if self.value == "A":
            return 11
        if self.value == "J" or self.value == "Q" or self.value == "K":
            return 10
        if int(self.value) in range(2,11):
            return int(self.value)
        raise ValueError("Cannot evaluate card with", self.value, "value.")
    
    def __str__(self):
        if self.suit == "clubs":
            str_suit = "♣"
        elif self.suit == "heart":
            str_suit = "♥"
        elif self.suit == "diamonds":
            str_suit = "♦"
        elif self.suit == "spades":
            str_suit = "♠"
        return str(self.value) + " " + str_suit


class Hand:
    def __init__(self, bet=MIN_BET):
        self.hand = []  # List of Card
        self.bet = bet

    def __iter__(self):
        return self.hand.__iter__()

    def __next__(self):
        return self.hand.__next__()

    def __len__(self):
        return len(self.hand)

    def __getitem__(self, key: int) -> Card:
        return self.hand[key]

    def pop(self):
        return self.hand.pop()

    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise TypeError("card must be of type Card")
        self.hand.append(card)

    def _get_num_aces(self):
        num_aces = 0
        for card in self.hand:
            if card.value == "A":
                num_aces += 1
        return num_aces

    @property
    def best_value(self):
        max_hand_value = sum(card.int_value for card in self.hand)
        if max_hand_value <= 21:
            return max_hand_value
        for num_aces in range(0, self._get_num_aces() + 1):
            if max_hand_value - (num_aces * 10) <= 21:
                return max_hand_value - (num_aces * 10)
        return max_hand_value - (self._get_num_aces() * 10)

    @property
    def second_best_value(self):
        max_hand_value = sum(card.int_value for card in self.hand)
        best_hand_value = self.best_value
        aces_used_in_best_hand = (max_hand_value - best_hand_value) // 10
        num_aces = self._get_num_aces()
        for ace_cnt in range(aces_used_in_best_hand + 1, num_aces + 1):
            if max_hand_value - (ace_cnt * 10) <= 21:
                return max_hand_value - (ace_cnt * 10)
        return max_hand_value - (num_aces * 10)

    def is_bust(self):
        return self.best_value > 21

    def is_blackjack(self):
        return self.best_value == 21 and len(self.hand) == 2

    def is_splitable(self):
        card1_value = self.hand[0].int_value
        card2_value = self.hand[1].int_value
        return len(self.hand) == 2 and card1_value == card2_value


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
        return len(self.deck)

    def __iter__(self):
        return self.deck.__iter__()

    def __next__(self):
        return self.deck.__next__()

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


def verify_player_hand_modifier(f):
    def wrapper(self):
        f(self)
    return wrapper


class Player:
    def __init__(self, bankroll=STARTING_CASH):
        self.bankroll = bankroll
        self.hands = [Hand()]  # list of Hand to handle splits
        self.active_hand_index = 0

    @property
    def hand(self):
        return self.hands[self.active_hand_index]

    def split_hand(self, card1, card2):
        assert self.hand.is_splitable()
        base_hand = self.hand
        bet = base_hand.bet
        new_hand = Hand(bet)
        new_hand.add_card(base_hand.pop())
        self.hands.insert(self.active_hand_index, new_hand)
        self.add_card_to_hand(card1)
        self.active_hand_index += 1
        self.add_card_to_hand(card2)

    def add_card_to_hand(self, card):
        card.showing = True
        self.hands[self.active_hand_index].add_card(card)

    def move_all_cards(self, destination: Deck):
        assert isinstance(destination, Deck)
        copy_hands = copy.deepcopy(self.hands)
        for hand_cnt, copy_hand in enumerate(copy_hands):
            for copy_card in copy_hand:
                copy_card.showing = False
                destination.append(copy_card)
                self.hands[hand_cnt].pop() # free actual card from original hand
        self.hands = [self.hands[0]] # don't leak memory


class Dealer:
    def __init__(self):
        self.hand = Hand()

    def add_card_to_hand(self, card):
        if len(self.hand) == 1:
            card.showing = True
        self.hand.add_card(card)

    @property
    def card_showing(self):
        return self.hand[1]

    def move_all_cards(self, destination: list()):
        copy_hand = copy.deepcopy(self.hand)
        for i, copy_card in enumerate(copy_hand):
            copy_card.showing = False
            destination.append(copy_card)
            self.hand.pop()


def playstatemethod(f):
    def wrapper(self):
        f(self)
        player = self.players[self.active_player_index]
        if player.hand.is_blackjack() or player.hand.is_bust():
            if player.active_hand_index > 0:
                self.stand_player()
            else:
                self.evaluate_hands()
                self.clear_table()
                self.deal_cards()
    return wrapper

class Game:
    def __init__(self):
        self.deck = Deck(NUM_DECKS_IN_GAME)
        self.discard_pile = Deck(0)
        self.dealer = Dealer()
        self.state = GameState.DEAL_CARDS   # helps view module
        player1 = Player(STARTING_CASH)
        self.players = [player1]  # list for expandability
        self.active_player_index = 0

    def deal_cards(self):
        for player in self.players:
            assert len(player.hand) == 0 and len(player.hands) == 1
        assert len(self.dealer.hand) == 0
        self.deck.deal_cards(self.players + [self.dealer])

    def clear_table(self):
        for player in self.players + [self.dealer]:
            player.move_all_cards(self.discard_pile)

    def evaluate_hands(self):
        dealer_score = self.dealer.hand.best_value

        for player in self.players:
            for hand in player.hands:
                if hand.is_blackjack() and not self.dealer.hand.is_blackjack():
                    player.bankroll += hand.bet * BLACKJACK_PAYS
                elif hand.is_bust():
                    player.bankroll -= hand.bet
                elif hand.best_value > dealer_score:
                    player.bankroll += hand.bet
                elif hand.best_value < dealer_score:
                    player.bankroll -= hand.bet
                else:
                    pass  # push, no money won, no money lost

    @playstatemethod
    def stand_player(self):
        player = self.players[self.active_player_index]
        if player.active_hand_index == 0:
            self.evaluate_hands()
            self.clear_table()
            self.deal_cards()
        else:
            player.active_hand_index -= 1

    @playstatemethod
    def hit_player(self):
        player_idx = self.active_player_index
        player = self.players[player_idx]
        assert not player.hand.is_bust()
        self.deck.hit(player)

    @playstatemethod
    def split_player(self):
        player_idx = self.active_player_index
        player = self.players[player_idx]
        assert len(player.hands) < MAX_SPLITS
        card1 = self.deck.pop()
        card2 = self.deck.pop()
        player.split_hand(card1, card2)
