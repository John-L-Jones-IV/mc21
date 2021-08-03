#!/usr/bin/env python3
from __future__ import annotations
from sys import exit

import pygame

import eventhandler as eventhandler
import gamelogic
import gamevariables as gv
import UI


def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(UI.FPS)  # Ensure while loop only executes per FPS timing.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            eventhandler.handle_event(event, gv, UI)

        gamelogic.handle_game_state(gv, UI)
        UI.draw_screen(gv)


if __name__ == "__main__":
    main()
