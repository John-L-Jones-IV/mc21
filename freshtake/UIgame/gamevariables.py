#!/usr/bin/env python3
from __future__ import annotations
import random

from gamevariabletypes import Card, Player, Dealer, GameState, build_draw_deck

NUM_DECKS_IN_GAME = 6
STARTING_CASH = 500
MIN_BET = 2
NUM_BOT_PLAYERS = 0
NUM_LOCAL_PLAYERS = 1

state = GameState.DEALING_CARDS
draw_deck = build_draw_deck(NUM_DECKS_IN_GAME)
discard_deck = []  # Empty list to hold dead cards before reshuffle.
player1 = Player(STARTING_CASH)
human_players = [player1]
dealer = Dealer()

bot_players = []

players = human_players + bot_players

def deal_cards():
    for _ in range(2):
        for player in [dealer] + players:
            player.add_card_to_hand(draw_deck.pop())

