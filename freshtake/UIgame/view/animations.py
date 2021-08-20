#!/usr/bin/evn python3 python
from __future__ import annotations
import math
import pygame
import sys

from mainGUI import clock
import view.GUI as GUI


def dealer_turn(game):
    pass


def move_card(card, start_pos, end_pos):
    VEL = 20
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    d_x = end_x - start_x
    d_y = end_y - start_y
    d = int(math.sqrt(d_x ** 2 + d_y ** 2))
    steps = round(d / VEL)
    x_step = round(d_x / steps)
    y_step = round(d_y / steps)

    x, y = start_x, start_y
    prev_x, prev_y = x, y
    while x != end_x or y != end_y:
        print(f"x: {x} y: {y}")
        clock.tick(GUI.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if (dist_left := end_x - x) > 0:
            if x_step > dist_left:
                x += dist_left
            else:
                x += x_step
        if (dist_left := end_y - y) > 0:
            if y_step > dist_left:
                y += dist_left
            else:
                y += y_step

        _cover_old_card((prev_x, prev_y))
        prev_x, prev_y = x, y
        GUI.draw_card(card, (x, y))
        pygame.display.flip()


def _cover_old_card(pos):
    x, y = pos
    cover_w, cover_h = 93, 139
    rect = pygame.Rect(x - 1, y - 1, cover_w, cover_h)
    pygame.draw.rect(GUI.window, GUI.GREEN, rect)
    GUI.draw_deck()
