#!/usr/bin/env python3
from __future__ import annotations
import os
import sys

import pygame

from model.classes import GameState
from .buttonclickedfunctions import (
    menu_button_clicked,
    hit_button_clicked,
    stand_button_clicked,
    surrender_button_clicked,
    split_button_clicked,
    double_button_clicked,
    deal_button_clicked,
)
from .guibutton import UIButton

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FPS = 120
HAND_STEP = 250  # x distance between each split hand drawn on screen

# Colors
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
RED = (0xFF, 0x00, 0x00)
BLUE = (0x00, 0x00, 0xFF)
GREEN = (0x55, 0xAA, 0x55)  # 55AA55 is from card asset source image.

# Fonts
pygame.font.init()
FONT_SIZE = 30
FONT = pygame.font.SysFont("comicsans", FONT_SIZE)


def draw_screen(game_vars):
    """Evaluate state and draw screen with pygame."""
    window.fill(GREEN)
    state = game_vars.state
    if state == GameState.MENU_AND_SETTINGS:
        pass
    elif state == GameState.PLACE_BETS:
        pass
    elif state == GameState.PLAY:
        draw_buttons(play_decission_buttons)
        draw_active_hand_indicator(game_vars.player1.active_hand)
        draw_players_hands(game_vars.player1.get_hands())
        draw_dealers_hand(game_vars.dealer.get_hand())
        draw_game_info(game_vars)
    elif state == GameState.EVALUATE_RESULTS:
        pass
    pygame.display.flip()


def draw_buttons(buttons):
    """Call draw() method for each button in list(buttons)"""
    for b_key in buttons:
        buttons[b_key].draw(window)


def draw_chip(surface, color, pos, radius, text):
    pygame.draw.circle(surface, color, pos, radius)
    x, y = pos
    text_img = FONT.render(text, False, WHITE)
    img_width, img_height = text_img.get_size()
    surface.blit(text_img, (x - img_width // 2, y - img_height // 2))


def draw_chips(surface):
    start_x, y = 200, 150
    radius = 25
    spacing = 100
    color = (0xAA, 0x22, 0x22)
    text = "100"
    for i in range(5):
        x = start_x + spacing * i
        pos = (x, y)
        draw_chip(surface, color, pos, radius, text)


def draw_card(
    window: pygame.Surface, card: gamevariabletypes.Card, pos: (x, y)
) -> None:
    suit, val = card.get_suit(), card.get_value_as_str()
    if card.showing:
        img_path = os.path.join("assets", "cards", suit + "_" + val + ".png")
    else:
        img_path = os.path.join("assets", "cardback.png")
    img = pygame.image.load(img_path)
    window.blit(img, pos)


def draw_players_hands(hands):
    start_x, x_step = 200, 35
    start_y, y_step = 550, -30
    start_hand = 400  # for splits
    for hand_cnt, hand in enumerate(hands):
        for card_cnt, card in enumerate(hand):
            x = start_x + card_cnt * x_step + hand_cnt * HAND_STEP
            y = start_y + card_cnt * y_step
            draw_card(window, card, (x, y))


def draw_active_hand_indicator(active_hand):
    brighter_green = (0x00, 0xFF, 0x00)
    start_x = 190
    width, height = 145, 200
    left = start_x + active_hand * HAND_STEP
    top = 500
    rect = pygame.Rect(left, top, width, height)
    pygame.draw.rect(window, brighter_green, rect)


def draw_dealers_hand(hand):
    start_x, x_step, start_y, y_step = 550, 50, 50, 0
    for cnt, card in enumerate(hand):
        x = start_x + cnt * x_step
        y = start_y + cnt * y_step
        draw_card(window, card, (x, y))


def draw_game_info(game_vars):
    x_start, y = 250, 690
    x_offset = HAND_STEP * game_vars.player1.active_hand
    x = x_start + x_offset
    soft_hand_value = game_vars.player1.get_soft_hand_value()
    hard_hand_value = game_vars.player1.get_hard_hand_value()

    if soft_hand_value != hard_hand_value and soft_hand_value <= 21:
        game_info_str = f"{soft_hand_value}/{hard_hand_value}"
    else:
        game_info_str = str(hard_hand_value)
    text_surface = FONT.render(game_info_str, False, (0, 0, 0))
    window.blit(text_surface, (x, y))


def define_UI_buttons():
    menu_btn = UIButton((10, 10, 100, 25), "Menu", menu_button_clicked)
    hit_btn = UIButton((20, 675, 100, 25), "Hit", hit_button_clicked)
    stand_btn = UIButton((20, 640, 100, 25), "Stand", stand_button_clicked)
    double_btn = UIButton((20, 605, 100, 25), "Double", double_button_clicked)
    surrender_btn = UIButton((20, 570, 100, 25), "Surrender", surrender_button_clicked)
    split_btn = UIButton((20, 535, 100, 25), "Split", split_button_clicked)

    return {
        "menu": menu_btn,
        "hit": hit_btn,
        "stand": stand_btn,
        "double": double_btn,
        "split": split_btn,
        "surrender": surrender_btn,
    }


pygame.init()
icon_img = pygame.image.load(os.path.join("assets", "blackjackicon.png"))
pygame.display.set_icon(icon_img)
pygame.display.set_caption("mc21 - Blackjack for Humans")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
play_decission_buttons = define_UI_buttons()
