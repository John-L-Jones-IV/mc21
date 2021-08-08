#!/usr/bin/env python3
from __future__ import annotations
from sys import exit
import pygame

import controller.eventhandler as eventhandler
import model.gamelogic as gamelogic
import model.gamevariables as game_vars
import view.GUI as GUI


clock = pygame.time.Clock()


def main():
    
    game_running = True

    while game_running:
        clock.tick(GUI.FPS)  # Ensure while loop only executes at FPS rate.
        process_user_input()
        gamelogic.handle_game_state(game_vars, GUI)
        GUI.draw_screen(game_vars)


def process_user_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        eventhandler.handle_event(event, game_vars, GUI)


if __name__ == "__main__":
    main()
