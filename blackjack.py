#!/usr/bin/env python3
"""
blackjack.py
Classes and functions for Blackjack simulations and game

John L. Jones IV
"""
import os
import random
from enum import IntEnum

VALS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['Clubs', 'Heart', 'Diamond', 'Spades']


class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def get_num_val(self, hard=False):
        if self.val == 'Blank':
            raise ValueError('Cannot evaluate card with', self.val, 'value')
        if self.val == 'A':
            if hard:
                return 1
            else:
                return 11
        if self.val == 'J' or self.val == 'Q' or self.val == 'K':
            return 10
        return int(self.val)

    def __str__(self):
        if self.val == 'Blank':
            return 'BLANK CARD'
        if self.suit == 'Clubs':
            str_suit = '♣'
        elif self.suit == 'Heart':
            str_suit = '♥'
        elif self.suit == 'Diamond':
            str_suit = '♦'
        elif self.suit == 'Spades':
            str_suit = '♠'
        return str(self.val) + ' ' + str_suit


class Status(IntEnum):
    STAND = 0
    PLAY = 1


class Player(object):
    def __init__(self, deck, used_cards):
        self.deck = deck                # list of Card as reference
        self.used_cards = used_cards    # list of Card as reference
        self.hand = []                  # list of Card for private use
        self.status = Status.PLAY
        self.wager = 0
        self.balence = 0

    def set_wager(self, wager):
        if type(wager) is not int or wager < 0:
            raise ValueError('wager must be an int greater than 0')
        self.wager = wager

    def reshuffle(self):
        self.deck.extend(self.used_cards)
        self.used_cards.clear()

        # if any blank cards are in the deck remove them
        for card in self.deck:
            if card.val == 'Blank':
                self.deck.remove(card)
                del card

        random.shuffle(self.deck)
        rand_index = 8 + random.randint(-4, 4)
        blank_card = Card('Plastic', 'Blank')
        self.deck.insert(rand_index, blank_card)

    def hit(self):
        card = self.deck.pop()
        if card.val == 'Blank':
            self.reshuffle()
            del card
            card = self.deck.pop()
        self.hand.append(card)

    def stand(self):
        self.status = Status.STAND

    def win(self, mult=1.0):
        self.balence += int(self.wager*mult)

    def lose(self, mult=1.0):
        self.balence -= int(self.wager*mult)

    def disp_hand(self):
        for card in self.hand:
            print(card)

    def hand_val(self, hard=False):
        """ returns the value of hand """
        val = 0
        for card in self.hand:
            val += card.get_num_val(hard=hard)
        return val

    def best_hand_val(self):
        """ returns most favorable value of hand """
        if self.hand_val(hard=True) > 21:
            return 0
        if self.hand_val() <= 21:
            return self.hand_val()
        return self.hand_val(hard=True)

    def has_blackjack(self):
        if self.hand_val() == 21 and len(self.hand) == 2:
            self.stand()
            return True

    def move(self):
        """ Implemented in child classes only """
        raise NotImplementedError

def build_deck():
    deck = []
    for _ in range(8):
        for val in VALS:
            for suit in SUITS:
                deck.append(Card(suit, val))
    random.shuffle(deck)
    blank_card = Card('Plastic', 'Blank')
    random_index = 8 + random.randint(-4, 4)
    deck.insert(random_index, blank_card)
    return deck


def deal_cards(players):
    """
    deal 2 cards to each Player in players
    players: a list of Player class
    """
    for _ in range(2):
        for player in players:
            player.hit()


def clear_table(players):
    for player in players:
        player.status = Status.PLAY
        while len(player.hand):
            player.used_cards.append(player.hand.pop())
