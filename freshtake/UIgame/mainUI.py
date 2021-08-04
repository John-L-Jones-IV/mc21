#!/usr/bin/env python3
from __future__ import annotations
from sys import exit
import pygame

import eventhandler
import gamelogic
import gamevariables as game_vars
import UI


def main():
    clock = pygame.time.Clock()
    game_running = True

    while game_running:
        clock.tick(UI.FPS)  # Ensure while loop only executes at FPS rate.
        process_user_input()
        gamelogic.handle_game_state(game_vars, UI)
        UI.draw_screen(game_vars)


def process_user_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        eventhandler.handle_event(event, game_vars, UI)


if __name__ == "__main__":
    main()
