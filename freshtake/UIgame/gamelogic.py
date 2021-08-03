#!/usr/bin/env python3
from __future__ import annotations
from classes import GameState
from gamevariables import MAX_SPLITS


def play_state(game_vars, ui):
    player = game_vars.player1
    if player.has_blackjack() or player.has_bust():
        if player.active_hand > 0:
            player.active_hand -= 1
        else:
            game_vars.state = GameState.EVALUATE_RESULTS
        return
    hand = player.get_hand()
    num_hands = len(player.get_hands())
    hand_len = len(hand)
    btns = ui.main_UI_buttons
    btns["split"].active = False
    if hand_len > 2:
        btns["surrender"].active = False
        btns["double"].active = False
    elif (
        hand_len == 2
        and hand[0].get_value() == hand[1].get_value()
        and num_hands <= MAX_SPLITS
    ):
        btns["split"].active = True


def handle_game_state(game_vars, ui):
    if game_vars.state == GameState.MENU_AND_SETTINGS:
        pass
    elif game_vars.state == GameState.PLACE_BETS:
        pass
    elif game_vars.state == GameState.DEAL_CARDS:
        game_vars.draw_deck.deal_cards(game_vars.players)
        game_vars.state = GameState.PLAY
    elif game_vars.state == GameState.PLAY:
        play_state(game_vars, ui)
    elif game_vars.state == GameState.EVALUATE_RESULTS:
        pass
