#!/usr/bin/env python3
from __future__ import annotations

from classes import GameState
from gamevariables import MAX_SPLITS


def handle_game_state(game_vars, ui):
    state = game_vars.state
    if state == GameState.MENU_AND_SETTINGS:
        pass
    elif state == GameState.PLACE_BETS:
        pass
    elif state == GameState.DEAL_CARDS:
        game_vars.deck.deal_cards(game_vars.players)
        game_vars.state = GameState.PLAY
    elif state == GameState.PLAY:
        play_state(game_vars, ui)
    elif state == GameState.EVALUATE_RESULTS:
        pass


def play_state(game_vars, ui):
    player = game_vars.player1
    more_split_hands = player.active_hand > 0

    if player.is_hand_blackjack() or player.is_hand_bust():
        if more_split_hands:
            player.active_hand -= 1
        else:
            game_vars.state = GameState.EVALUATE_RESULTS
        return

    update_play_state_buttons_activation_status(game_vars, ui)


def update_play_state_buttons_activation_status(game_vars, ui):
    player = game_vars.player1
    hand = player.get_hand()
    num_hands = len(player.get_hands())
    hand_len = len(hand)
    btns = ui.play_decission_buttons

    can_surrender = hand_len == 2 and num_hands == 1
    if can_surrender:
        btns["surrender"].set_active(True)
    else:
        btns["surrender"].set_active(False)

    if hand_len > 2:
        btns["double"].set_active(False)
    elif hand_len == 2:
        btns["double"].set_active(True)

    can_split = (
        hand_len == 2
        and num_hands <= MAX_SPLITS
        and hand[0].get_value() == hand[1].get_value()
    )
    if can_split:
        btns["split"].set_active(True)
    else:
        btns["split"].set_active(False)
