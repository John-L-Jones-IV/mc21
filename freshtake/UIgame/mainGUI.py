#!/usr/bin/env python3
from __future__ import annotations

import pygame

from model.blackjackcore import Game
import view.GUI as GUI


clock = pygame.time.Clock()


def main():
    GUI.init()
    game = Game()
    game.deal_cards()
    while True:
        clock.tick(GUI.FPS)  # Ensure while loop only executes at FPS rate.
        GUI.process_user_input(game)
        GUI.monitor_changes(game)
        GUI.draw_screen(game)

if __name__ == "__main__":
    main()
