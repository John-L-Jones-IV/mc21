#!/usr/bin/env python3
from __future__ import annotations
from sys import exit
import pygame

from model.blackjackcore import Game
import view.GUI as GUI  # FIXME: singleton?


clock = pygame.time.Clock()


def main():
    game = Game()
    game.deal_cards()
    while True:
        clock.tick(GUI.FPS)  # Ensure while loop only executes at FPS rate.
        process_user_input(game)
        GUI.draw_screen(game)


def process_user_input(game):
    """Handle pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        handle_event(event, game)


def handle_event(event, game):
    """Handle pygame events and send user request to blackjackcore."""
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        btns = GUI.play_decission_buttons
        for _, btn in btns.items():
            if btn.is_mouse_position_colliding(mouse_pos):
                btn.function(game)


if __name__ == "__main__":
    main()
