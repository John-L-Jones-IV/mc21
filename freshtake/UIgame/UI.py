#!/usr/bin/env python3
from __future__ import annotations

import pygame
import os


WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FPS = 120
FONT_SIZE = 30

pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 30)

# Colors
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
RED = (0xFF, 0x00, 0x00)
BLUE = (0x00, 0x00, 0xFF)
GREEN = (0x55, 0xAA, 0x55)  # 55AA55 is from card asset source image.


def draw_buttons(window, buttons):
    for b_key in buttons:
        buttons[b_key].draw(window)


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


class UIButton:
    # static attributes, same for all instances of UIButton.
    BORDER_RADIUS = 5
    ACTIVE_TEXT_COLOR = BLACK
    NON_ACTIVE_TEXT_COLOR = BLACK
    ACTIVE_BTN_COLOR = (0xAA, 0xAA, 0xAA)
    NON_ACTIVE_BTN_COLOR = (0x55, 0x55, 0x55)

    def __init__(self, dimensions, text, function):
        self.active = True
        self.hidden = False
        x_position, y_position, width, height = dimensions
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.text = text
        self.function = function

    def get_dimensions(self):
        return (self.x_position, self.y_position, self.width, self.height)

    def mouse_pos_on_button(self, mouse_pos: (mouse_x, mouse_y)) -> bool:
        if self.hidden or not self.active:
            return False
        mouse_x, mouse_y = mouse_pos
        if not (self.x_position <= mouse_x <= self.x_position + self.width):
            return False
        if not (self.y_position <= mouse_y <= self.y_position + self.height):
            return False
        return True

    def draw(self, surface):
        if self.hidden:
            return
        x, y, w, h = self.get_dimensions()
        rect = pygame.Rect(x, y, w, h)
        self._draw_button(surface, rect)
        self._draw_text(surface, rect)

    @staticmethod
    def _find_pos_of_smaller_rect_centered(
        large_rect: pygame.Rect(), small_rect: pygame.Rect()
    ) -> (x_pos, y_pos):
        """
        Given a large and small rectangle return the position needed
        to place the small rectange directly in the center of the large
        rectangle.

        Use to center the text image on the button image for UIButton.
        """
        large_width, large_height = large_rect.size
        small_width, small_height = small_rect.size
        x_offset = (large_width - small_width) / 2
        y_offset = (large_height - small_height) / 2
        small_x = int(large_rect.x + x_offset)
        small_y = int(large_rect.y + y_offset)
        return small_x, small_y

    def _draw_button(self, surface, rect):
        color = self.ACTIVE_BTN_COLOR if self.active else self.NON_ACTIVE_BTN_COLOR
        pygame.draw.rect(surface, color, rect, border_radius=UIButton.BORDER_RADIUS)

    def _draw_text(self, surface, rect):
        if self.active:
            text_color = self.ACTIVE_TEXT_COLOR
        else:
            text_color = self.NON_ACTIVE_TEXT_COLOR
        font = pygame.font.SysFont(None, FONT_SIZE)
        text_img = font.render(self.text, True, text_color)
        text_rect = text_img.get_rect()
        text_x, text_y = UIButton._find_pos_of_smaller_rect_centered(rect, text_rect)
        surface.blit(text_img, (text_x, text_y))


def menu_button_clicked(game_vars):
    print("menu button clicked!")


def hit_button_clicked(game_vars):
    print("hit button clicked!")
    game_vars.draw_deck.hit(game_vars.player1)


def stand_button_clicked(game_vars):
    print("stand button clicked!")
    if game_vars.player1.active_hand > 0:
        game_vars.player1.active_hand -= 1
    else:
        game_vars.state = game_vars.GameState.EVALUATE_HANDS


def surrender_button_clicked(game_vars):
    print("surrender button clicked!")


def split_button_clicked(game_vars):
    print("split button clicked!")
    deck = game_vars.draw_deck
    player = game_vars.player1
    player.split_hand()
    for i in range(-1, -3, -1):
        card = deck.pop()
        card.set_showing(True)
        player.hands[i].append(card)


def double_button_clicked(game_vars):
    print("double button clicked!")


def deal_button_clicked(game_vars):
    print("deal button clicked!")


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


def draw_players_hands(window, hands):
    start_x, x_step = 200, 35
    start_y, y_step = 550, -30
    start_hand, hand_step = 400, 250  # for splits
    for hand_cnt, hand in enumerate(hands):
        for card_cnt, card in enumerate(hand):
            x = start_x + card_cnt * x_step + hand_cnt * hand_step
            y = start_y + card_cnt * y_step
            draw_card(window, card, (x, y))

def draw_active_hand_indicator(window, active_hand):
    brighter_green = (0x00, 0xFF, 0x00)
    hand_step = 250
    start_x = 190
    width, height = 145, 200
    left = start_x + active_hand * hand_step
    top = 500
    rect = pygame.Rect(left, top, width, height)
    pygame.draw.rect(window, brighter_green, rect)


def draw_dealers_hand(window, hand):
    start_x, x_step, start_y, y_step = 550, 50, 50, 0
    for cnt, card in enumerate(hand):
        x = start_x + cnt * x_step
        y = start_y + cnt * y_step
        draw_card(window, card, (x, y))


def draw_game_info(window, game_vars):
    x, y = 250, 690
    hand_val_str = "test"
    game_info_str = f"Bankroll: {game_vars.player1.bankroll}Hand value:{hand_val_str}"
    text_surface = FONT.render(game_info_str, False, (0, 0, 0))
    window.blit(text_surface, (x, y))


def draw_screen(game_vars):
    window.fill(GREEN)
    if game_vars.state == game_vars.GameState.MENU_AND_SETTINGS:
        pass
    elif game_vars.state == game_vars.GameState.PLACE_BETS:
        draw_popup_menu(window)
    elif game_vars.state == game_vars.GameState.DEAL_CARDS:
        pass
    elif game_vars.state == game_vars.GameState.PLAY:
        draw_buttons(window, main_UI_buttons)
        draw_active_hand_indicator(window, game_vars.player1.active_hand)
        draw_players_hands(window, game_vars.player1.get_hands())
        draw_dealers_hand(window, game_vars.dealer.get_hand())
        draw_game_info(window, game_vars)
    elif game_vars.state == game_vars.GameState.EVALUATE_RESULTS:
        pass
    pygame.display.flip()


pygame.init()
icon_img = pygame.image.load(os.path.join("assets", "blackjackicon.png"))
pygame.display.set_icon(icon_img)
pygame.display.set_caption("mc21 - Blackjack for Humans")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
main_UI_buttons = define_UI_buttons()
