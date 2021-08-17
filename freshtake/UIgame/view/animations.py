#!/usr/bin/evn python3 python
from __future__ import annotations

import view.GUI as GUI
import pygame
from mainGUI import clock, process_user_input


def play_evaluate_hands(game_vars):
    for i in range(30):
        clock.tick(GUI.FPS)
        process_user_input()
        GUI.window.fill(GUI.GREEN)
        GUI.draw_chips(GUI.window)
        pygame.display.flip()


def _move_card(card, start_pos, end_pos, frames):
    start_x, start_y = start_pos
    end_x, end_y = end_pos
