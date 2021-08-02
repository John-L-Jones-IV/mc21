#!/usr/bin/env python3
from __future__ import annotations

import pygame
import os


WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FPS = 120
FONT_SIZE = 30

# Colors
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
RED = (0xFF, 0x00, 0x00)
BLUE = (0x00, 0x00, 0xFF)
GREEN = (0x55, 0xAA, 0x55)  # 55AA55 is from card asset source image.


def card_img_lookup(suit: str, val: str) -> pygame.image:
    assert val in CARD_VALS
    assert suit in CARD_SUITS
    img_path = os.path.join("assets", "cards", suit + "_" + val + ".png")
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
    return img


def draw_buttons(window, buttons):
    for btn in buttons:
        btn.draw(window)


def define_UI_buttons():
    menu_btn = UIButton((10, 10, 100, 25), "Menu", menu_button_clicked)
    hit_btn = UIButton((20, 650, 100, 25), "Hit", hit_button_clicked)
    stand_btn = UIButton((20, 600, 100, 25), "Stand", stand_button_clicked)
    double_btn = UIButton((20, 550, 100, 25), "Double", double_button_clicked)
    surrender_btn = UIButton((20, 500, 100, 25), "Surrender", surrender_button_clicked)
    split_btn = UIButton((20, 450, 100, 25), "Split", split_button_clicked)
    surrender_btn.active = False

    return [menu_btn, hit_btn, stand_btn, double_btn, split_btn, surrender_btn]


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


def define_bet_menu_buttons():
    # red chips
    menu_btn = UIButton((10, 10, 100, 25), "+5", increase_bet, 5, RED_CHIP)
    menu_btn = UIButton((10, 10, 100, 25), "-5", menu_button_clicked, -5, RED_CHIP)
    # blue chips
    menu_btn = UIButton((10, 10, 100, 25), "+10", menu_button_clicked, 10, BLUE_CHIP)
    menu_btn = UIButton((10, 10, 100, 25), "-10", menu_button_clicked, -10, BLUE_CHIP)
    # green chips
    menu_btn = UIButton((10, 10, 100, 25), "+25", menu_button_clicked, 25, GREEN_CHIP)
    menu_btn = UIButton((10, 10, 100, 25), "-25", menu_button_clicked, -25, GREEN_CHIP)
    # orange chips
    menu_btn = UIButton((10, 10, 100, 25), "+50", menu_button_clicked, 50, ORANGE_CHIP)
    menu_btn = UIButton((10, 10, 100, 25), "-50", menu_button_clicked, -50, ORANGE_CHIP)
    # black chips
    menu_btn = UIButton((10, 10, 100, 25), "+100", menu_button_clicked, 100, BLACK_CHIP)
    menu_btn = UIButton((10, 10, 100, 25), "-100", menu_button_clicked, 100, BLACK_CHIP)

    deal_btn = UIButton((20, 450, 100, 25), "Deal", deal_button_clicked)


class UIButton:
    # static attributes, same for all instances of UIButton.
    BORDER_RADIUS = 5
    ACTIVE_TEXT_COLOR = BLACK
    NON_ACTIVE_TEXT_COLOR = BLACK
    ACTIVE_BTN_COLOR = (0xAA, 0xAA, 0xAA)
    NON_ACTIVE_BTN_COLOR = (0x55, 0x55, 0x55)

    @staticmethod
    def find_pos_of_smaller_rect_centered(
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
        text_x, text_y = UIButton.find_pos_of_smaller_rect_centered(rect, text_rect)
        surface.blit(text_img, (text_x, text_y))

    def draw(self, surface):
        if self.hidden:
            return
        x, y, w, h = self.get_dimensions()
        rect = pygame.Rect(x, y, w, h)
        self._draw_button(surface, rect)
        self._draw_text(surface, rect)


def menu_button_clicked(game_vars, ui):
    print("menu button clicked!")


def hit_button_clicked(game_vars, ui):
    game_vars.player1.add_card_to_hand(game_vars.draw_deck.pop())
    print("hit button clicked!")


def stand_button_clicked(game_vars, ui):
    print("stand button clicked!")


def surrender_button_clicked(game_vars, ui):
    print("surrender button clicked!")


def split_button_clicked(game_vars, ui):
    print("split button clicked!")


def double_button_clicked(game_vars, ui):
    print("double button clicked!")


def deal_button_clicked(game_vars, ui):
    print("deal button clicked!")


def draw_popup_menu(window):
    pass  # TODO

def draw_card(window: pygame.Surface, card: gamevariabletypes.Card, pos: (x, y)) -> None:
    suit, val = card.get_suit(), card.get_val()
    if card.showing:
        img_path = os.path.join("assets", "cards", suit + "_" + val + ".png")
    else:
        img_path = os.path.join("assets", "cardback.png")
    img = pygame.image.load(img_path)
    window.blit(img, pos)



def draw_players_hand(window, hand):
    start_x, x_step, y = 200, 100, 500
    for cnt, card in enumerate(hand):
        x = start_x + cnt * x_step
        draw_card(window, card, (x,y))

def draw_dealers_hand(window, hand):
    start_x, x_step, y = 550, 100, 100
    for cnt, card in enumerate(hand):
        x = start_x + cnt * x_step
        draw_card(window, card, (x,y))


def draw_screen(game_vars):
    window.fill(GREEN)
    if game_vars.state == game_vars.GameState.MENU_AND_SETTINGS:
        pass
    elif game_vars.state == game_vars.GameState.PLACING_BETS:
        draw_popup_menu(window)
    elif game_vars.state == game_vars.GameState.DEALING_CARDS:
        pass
    elif game_vars.state == game_vars.GameState.PLAYERS_PLAYING:
        draw_buttons(window, main_UI_buttons)
        draw_players_hand(window, game_vars.player1.get_hand())
        draw_dealers_hand(window, game_vars.dealer.get_hand())
    elif game_vars.state == game_vars.GameState.DEALER_PLAYING:
        pass
    elif game_vars.state == game_vars.GameState.EVALUATING_RESULTS:
        pass
    elif game_vars.state == game_vars.GameState.SETTLING_BETS:
        pass
    elif game_vars.state == game_vars.GameState.CLEARING_TABLE:
        pass
    pygame.display.flip()


pygame.init()
icon_img = pygame.image.load(os.path.join("assets", "blackjackicon.png"))
pygame.display.set_icon(icon_img)
pygame.display.set_caption("mc21 - Blackjack for Humans")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
main_UI_buttons = define_UI_buttons()
