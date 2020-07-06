#!/usr/bin/env python3
"""
Players.py
Player classes for Blackjack simulations and game

John L. Jones IV
"""
import random
from blackjack import Card, Player, Status


class Dealer(Player):
    def __init__(self, deck, used_cards):
        self.deck = deck                # list of Card as reference
        self.used_cards = used_cards    # list of Card as reference
        self.hand = []                  # list of Card for private use
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

#  class BasicStratPlayer(Player):
#      def __init__(self, balence, deck, used_cards, dealer):
#          """
#          Used strategy from wizzard of odds.
#          https://wizardofodds.com/games/blackjack/strategy/4-decks/
#          """
#          Player.__init__(self, deck, used_cards)
#          self.dealer = dealer
#  
#      def move(self):
#          dealer_showing = self.dealer.hand[0].get_num_val()
#          if self.best_hand_val() == 0:
#              self.stand()
#          # SPLITS
#          elif ((len(self.hand) == 2 and self.hand[0].val == self.hand[1].val and
#                  len(self.split_hand) == 0) and self.status == Status.PLAY and
#                  not (self.hand[0].val == 'J' or
#                       self.hand[0].val == '5' or self.hand[0].val == 'K' or
#                       self.hand[0].val == 'Q' or self.hand[0].val == '10')):
#              card_val = self.hand[0].val
#              if card_val == 'A':
#                  self.split()
#              elif card_val == '8':
#                  self.split()
#              elif card_val == '9':
#                  if (dealer_showing == 7 or
#                          10 <= dealer_showing <= 11):
#                      self.stand()
#                  else:
#                      self.split()
#              elif card_val == '7':
#                  if dealer_showing <= 7:
#                      self.split()
#                  else:
#                      self.hit()
#              elif card_val == '6':
#                  if dealer_showing <= 6:
#                      self.split()
#                  else:
#                      self.hit()
#              elif card_val == '4':
#                  if 5 <= dealer_showing <= 6:
#                      self.split()
#                  else:
#                      self.hit()
#              elif card_val == '2' or card_val == '3':
#                  if dealer_showing <= 7:
#                      self.split()
#                  else:
#                      self.hit()
#          # SOFT
#          elif (14 <= self.hand_val(hard=False) <= 21 and
#                self.hand_val(hard=False) != self.hand_val(hard=True)):
#              soft_val = self.hand_val(hard=False)
#              if soft_val >= 19:
#                  self.stand()
#              elif 9 <= dealer_showing <= 11:
#                  self.hit()
#              elif soft_val == 18:
#                  if 3 <= dealer_showing <= 6:
#                      self.double()
#                  else:
#                      self.stand()
#              elif 7 <= dealer_showing:
#                  self.hit()
#              elif soft_val == 17:
#                  if dealer_showing == 2:
#                      self.hit()
#                  else:
#                      self.double()
#              elif 15 <= soft_val <= 16:
#                  if 2 <= dealer_showing <= 3:
#                      self.hit()
#                  else:
#                      self.double()
#              elif soft_val == 14:
#                  if 2 <= dealer_showing <= 4:
#                      self.hit()
#                  else:
#                      self.double()
#          # HARD
#          else:
#              hand_val = self.hand_val()
#              if hand_val >= 17:
#                  self.stand()
#              elif 13 <= hand_val <= 16:
#                  if dealer_showing <= 6:
#                      self.stand()
#                  else:
#                      self.hit()
#              elif hand_val == 12:
#                  if 4 <= dealer_showing <= 6:
#                      self.stand()
#                  else:
#                      self.hit()
#              elif hand_val == 11:
#                  if dealer_showing == 11:
#                      self.hit()
#                  else:
#                      self.double()
#              elif hand_val == 10:
#                  if dealer_showing >= 10:
#                      self.hit()
#                  else:
#                      self.double()
#              elif hand_val == 9:
#                  if 3 <= dealer_showing <= 6:
#                      self.double()
#                  else:
#                      self.hit()
#              else:
#                  self.hit()
