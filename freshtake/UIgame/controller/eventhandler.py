#!/usr/bin/env python3
from __future__ import annotations

import pygame

from model.classes import GameState


def handle_event(event, game_vars, ui):
    # more like read pygame events?
    """Handle pygame events from user input.

    Evaluate GameState and execute accordingly."""
    if game_vars.state == GameState.MENU_AND_SETTINGS:
        pass
    elif game_vars.state == GameState.PLACE_BETS:
        pass
    elif game_vars.state == GameState.PLAY:
        handle_play_event(event, game_vars, ui)
    # no user input for other game states.


def handle_play_event(event, game_vars, ui):
    """handle pygame events for PLAY GameState"""
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        btns = ui.play_decission_buttons
        for _, btn in btns.items():
            if btn.is_mouse_position_colliding(mouse_pos):
                btn.function(game_vars)
