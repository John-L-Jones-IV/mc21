#!/usr/bin/env python3
from __future__ import annotations
from sys import exit

import os
import pygame
import random

import UI
import gamevariables as gv
import eventhandler as eh


def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(UI.FPS)  # Ensure while loop only executes per FPS timing.

        eh.handle_game_state(gv)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            eh.handle_event(event, gv, UI)

        UI.draw_screen(gv)


if __name__ == "__main__":
    main()
