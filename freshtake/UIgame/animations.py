#!/usr/bin/evn python3 python
from __future__ import annotations

import UI
import pygame
from mainUI import clock, process_user_input

def play_evaluate_hands(game_vars):
    for i in range(120):
        clock.tick(UI.FPS)
        process_user_input()
        UI.window.fill(UI.GREEN)
        UI.draw_chips(UI.window)
        pygame.display.flip()
