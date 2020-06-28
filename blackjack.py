#!/usr/bin/env python3
"""
blackjack.py
Classes and functions for Blackjack simulations and game

John L. Jones IV
"""
from enum import IntEnum
import random, os

VALS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10','J', 'Q', 'K']
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


class Status(IntEnum):
    STAND = 0
    PLAY = 1


class Player(object):
    def __init__(self, deck, used_cards):
        self.deck = deck                #  list of Card as reference
        self.used_cards = used_cards    #  list of Card as reference
        self.hand = []                  #  list of Card for private use
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

    def win(self, mult =1.0):
        self.balence += int(self.wager*mult)

    def lose(self, mult =1.0):
        self.balence -= int(self.wager*mult)

    def disp_hand(self):
        for card in self.hand:
            print(card)

    def hand_val(self, hard =False):
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


class Dealer(Player):
    def __init__(self, deck, used_cards):
        self.deck = deck                #  list of Card as reference
        self.used_cards = used_cards    #  list of Card as reference
        self.hand = []                  #  list of Card for private use
        self.status = Status.PLAY

    def move(self):
        """ Dealer hits until 17 or more """
        if self.best_hand_val() >= 17 or self.best_hand_val() == 0:
            self.stand()
        else:
            self.hit()


class SimplePlayer(Player):
    def __init__(self, deck, used_cards):
        Player.__init__(self, deck, used_cards)

    def move(self):
        """ SimplePlayer hits until 17 or more """
        if self.best_hand_val() >= 17 or self.best_hand_val() == 0:
            self.stand()
        else:
            self.hit()


class BasicStratPlayer(Player):
    """ Strategy Board Player """
    def __init__(self, deck, used_cards, dealer):
        Player.__init__(self, deck, used_cards)
        self.dealer = dealer #  refernce to Dealer, used to see card showing

    def move(self):
        dealer_showing = self.dealer.hand[0].get_num_val()
        if self.best_hand_val() == 0:
            self.stand()

        # SOFT Hand
        elif (14 <= self.hand_val(hard=False) <= 21 and
                self.hand_val(hard=False) !=  self.hand_val(hard=True)):
            print('inf loop')
            self.disp_hand()
            print(self.status)
            soft_val = self.hand_val(hard=False)
            if soft_val >= 19:
                self.stand()
            elif 9 <= dealer_showing <= 11:
                self.hit()
            elif soft_val == 18:
                if 3 <= dealer_showing <= 6:
                    self.double()
                else:
                    self.stand()
            elif 7 <= dealer_showing:
                self.hit()
            elif soft_val == 17:
                if dealer_showing == 2:
                    self.hit()
                else:
                    self.double()
            elif 15 <= soft_val <= 16:
                if 2 <= dealer_showing <= 3:
                    self.hit()
                else:
                    self.double()
            elif soft_val == 14:
                if 2 <= dealer_showing <= 4:
                    self.hit()
                else:
                    self.double()
        # HARD
        else:
            hand_val = self.hand_val()
            if hand_val >= 17:
                self.stand()
            elif 13 <= hand_val <= 16:
                if dealer_showing <= 6:
                    self.stand()
                else:
                    self.hit()
            elif hand_val == 12:
                if 4 <= dealer_showing <= 6:
                    self.stand()
                else:
                    self.hit()
            elif hand_val == 11:
                if dealer_showing == 11:
                    self.hit()
                else:
                    self.double()
            elif hand_val == 10:
                if dealer_showing >= 10:
                    self.hit()
                else:
                    self.double()
            elif hand_val == 9:
                if 3 <= dealer_showing <= 6:
                    self.double()
                else:
                    self.hit()
            else:
                self.hit()


class CCPlayer(Player):
    """ Card Counting Player """
    def __init__(self, balence, deck, used_cards, cards_showing, dealer):
        Player.__init__(balence, deck, used_cards, cards_showing)
        self.dealer = dealer

    def expected_return(self):
        """ Return expected return of bet given the remaining deck
        for each permutations of the remaining deck calculate expected return
        and then calculate the average
        """
        pass # TODO

    def move(self):
        pass # TODO

    def set_wager(self, wager):
        pass # TODO


class HLPlayer(BasicStratPlayer):
    """ player using high low counting system """
    def __init__(self, balence, deck, used_cards, cards_showing, dealer):
        BasicStratPlayer.__init__(
                self,
                balence,
                deck,
                used_cards,
                cards_showing,
                dealer
            )

    def set_wager(self, wager):
        running_cnt = 0
        for card in self.deck:
            if card.val == 'Blank':
                continue
            val = card.get_num_val()
            if 2 <= val <= 6:
                running_cnt += 1
            elif 10 <= val <= 11:
                running_cnt -= 1
        L = len(self.deck)
        decks_remaining = L//26
        decks_remaining = 1 if decks_remaining < 1 else decks_remaining
        tru_cnt = running_cnt/float(decks_remaining)
        bet = wager*(tru_cnt)
        if bet < 1:
            bet = wager
        if bet > 50:
            bet = 50
        self.wager = bet


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


def print_UI(dealer, player1, dealer_move=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Balence:', player1.balence)
    print('Wager:', player1.wager, '\n')
    print()
    if dealer_move:
        print('Dealer showing:', dealer.best_hand_val())
        dealer.disp_hand()
        print()
    else:
        print('Dealer showing:\n'+str(dealer.hand[0]), '\n')
    print('Your hand:', player1.best_hand_val())
    player1.disp_hand()
