#!/usr/bin/env python3
from __future__ import annotations
import random

from classes import Card, Player, Dealer, GameState, Deck

NUM_DECKS_IN_GAME = 6
STARTING_CASH = 200
MIN_BET = 5
MAX_SPLITS = 4

deck = Deck(NUM_DECKS_IN_GAME)
discard_pile = Deck(0)
player1 = Player(STARTING_CASH)
players = [player1]
dealer = Dealer()
state = GameState.DEAL_CARDS
