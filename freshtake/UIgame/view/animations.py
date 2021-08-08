#!/usr/bin/evn python3 python
from __future__ import annotations

import view.GUI as GUI
import pygame
from mainUI import clock, process_user_input

def play_evaluate_hands(game_vars):
    for i in range(30):
        clock.tick(GUI.FPS)
        process_user_input()
        GUI.window.fill(GUI.GREEN)
        GUI.draw_chips(GUI.window)
        pygame.display.flip()
