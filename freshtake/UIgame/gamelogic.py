#!/usr/bin/env python3
from __future__ import annotations

import animations
from classes import GameState, Player, Dealer
from gamevariables import MAX_SPLITS

def handle_game_state(game_vars, ui):
    state = game_vars.state
    if state == GameState.MENU_AND_SETTINGS:
        pass
    elif state == GameState.PLACE_BETS:
        pass
    elif state == GameState.DEAL_CARDS:
        all_players = game_vars.players + [game_vars.dealer]
        game_vars.deck.deal_cards(all_players)
        game_vars.state = GameState.PLAY
    elif state == GameState.PLAY:
        play_state(game_vars, ui)
        update_play_state_buttons_activation_status(game_vars, ui)
    elif state == GameState.EVALUATE_RESULTS:
        evaluate_results_state(game_vars, ui)
        animations.play_evaluate_hands(game_vars)
        clear_table(game_vars)
        game_vars.state = GameState.DEAL_CARDS

def clear_table(game_vars):
    all_players = game_vars.players + [game_vars.dealer]
    discard_pile = game_vars.discard_pile
    for player in all_players:
        player.move_all_cards(discard_pile)


def play_state(game_vars, ui):
    player = game_vars.player1
    more_split_hands = player.active_hand > 0

    if player.is_hand_blackjack() or player.is_hand_bust():
        if more_split_hands:
            player.active_hand -= 1
        else:
            game_vars.state = GameState.EVALUATE_RESULTS
        return


def evaluate_results_state(game_vars, ui):
    update_evaluate_state_buttons_activation_status(ui)
    animations.play_evaluate_hands(game_vars)
    #update_play_state_activation_status(ui)
    for hand in game_vars.player1.get_hands():
        print('eval hand:', hand) 
        


def update_evaluate_state_buttons_activation_status(ui):
    for _, btn in ui.play_decission_buttons.items():
        btn.set_active(False)


def update_play_state_buttons_activation_status(game_vars, ui):
    player = game_vars.player1
    hand = player.get_hand()
    num_hands = len(player.get_hands())
    hand_len = len(hand)
    btns = ui.play_decission_buttons

    # hit always active in play state
    btns["hit"].set_active(True)

    # stand always active in play state
    btns["stand"].set_active(True)

    is_surrender_btn_active = hand_len == 2 and num_hands == 1
    btns["surrender"].set_active(is_surrender_btn_active)

    is_double_btn_active = hand_len = 2
    btns["double"].set_active(is_double_btn_active)

    is_split_btn_active = (
        hand_len == 2
        and num_hands <= MAX_SPLITS
        and hand[0].get_value() == hand[1].get_value()
    )
    btns["split"].set_active(is_split_btn_active)
