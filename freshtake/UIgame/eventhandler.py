#!/usr/bin/env python3
from __future__ import annotations

import pygame

from gamevariabletypes import GameState

def set_buttons_hidden(buttons: list(Button), hiddenState: bool) -> None:
    for btn in buttons:
        btn.hidden = hiddenState


def update_hidden_UIs():
    if gv.state == gv.GameState.MENU_AND_SETTINGS:
        pass
    elif gv.state == gv.GameState.PLACING_BETS:
        set_buttons_active(UI.main_UI_buttons, False)
    elif gv.state == gv.GameState.MENU_AND_SETTINGS:
        pass
    elif gv.state == gv.GameState.MENU_AND_SETTINGS:
        pass
    elif gv.state == gv.GameState.MENU_AND_SETTINGS:
        pass
    elif gv.state == gv.GameState.MENU_AND_SETTINGS:
        pass
    elif gv.state == gv.GameState.MENU_AND_SETTINGS:
        pass
    elif gv.state == gv.GameState.MENU_AND_SETTINGS:
        pass


def handle_bet_button_event(event, bet_buttons):
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        for btn in bet_buttons:
            if btn.mouse_pos_on_button(mouse_pos):
                btn.function(btn.bet_size)


def handle_main_UI_event(event, game_vars, ui):
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        for btn in ui.main_UI_buttons:
            if btn.mouse_pos_on_button(mouse_pos):
                btn.function(game_vars, ui)

def handle_event(event, game_vars, ui):
    if game_vars.state == game_vars.GameState.MENU_AND_SETTINGS:
        pass
    elif game_vars.state == game_vars.GameState.PLACING_BETS:
        pass
    elif game_vars.state == game_vars.GameState.DEALING_CARDS:
        pass
    elif game_vars.state == game_vars.GameState.PLAYERS_PLAYING:
        handle_main_UI_event(event, game_vars, ui)
    elif game_vars.state == game_vars.GameState.DEALER_PLAYING:
        pass
    elif game_vars.state == game_vars.GameState.EVALUATING_RESULTS:
        pass
    elif game_vars.state == game_vars.GameState.SETTLING_BETS:
        pass
    elif game_vars.state == game_vars.GameState.CLEARING_TABLE:
        pass

def handle_game_state(game_vars):
    if game_vars.state == GameState.DEALING_CARDS:
        game_vars.deal_cards()
        game_vars.state = GameState.PLAYERS_PLAYING

