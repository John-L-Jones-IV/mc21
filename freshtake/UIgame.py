#!/usr/bin/env python3
from __future__ import annotations
from enum import IntEnum
from enum import auto
from sys import exit

import os
import pygame
import random

# TODO:
#   1. resize native card assests to 100x150 px or smaller

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
FPS = 120
FONT_SIZE = 30

# Color Constants
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
RED = (0xFF, 0x00, 0x00)
BLUE = (0x00, 0x00, 0xFF)
GREEN = (0x55, 0xAA, 0x55)  # 55AA55 is from card asset source image.

# Card types
CARD_VALS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_SUITS = ["hearts", "spades", "clubs", "diamonds"]

# Card aspect ratio should be 1:1.5
CARD_WIDTH, CARD_HEIGHT = 100, 150

NUM_DECKS_IN_GAME = 6
STARTING_CASH = 500
MIN_BET = 2


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
        if self.hidden:
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


class Card:
    def __init__(self, suit, val):
        assert suit in CARD_SUITS
        assert val in CARD_VALS
        self.suit = suit
        self.val = val

    def get_num_val(self, hard=False):
        if self.val == "blank":
            raise ValueError("Cannot evaluate card with", self.val, "value.")
        if self.val == "A":
            if hard:
                return 1
            else:
                return 11
        if self.val == "J" or self.val == "Q" or self.val == "K":
            return 10
        return int(self.val)


class Player:
    def __init__(self):
        self.hands = [[]]  # list of lists of cards, multiple for split hands.
        self.bank = STARTING_CASH
        self.bet = MIN_BET


class Dealer:
    hand = []  # list of cards


class GameStage(IntEnum):
    MENU_AND_SETTINGS = auto()
    PLACING_BETS = auto()
    DEALING_CARDS = auto()
    PLAYERS_PLAYING = auto()
    DEALER_PLAYING = auto()
    EVALUATING_RESULTS = auto()
    SETTLING_BETS = auto()


class GameState:
    def __init__(
        self,
        human_players: list(Player),
        dealer: Dealer,
        draw_deck: list(Card),
        discard_deck: list(),
    ):
        self.stage = GameStage.PLACING_BETS
        self.human_players = human_players
        self.dealer = Dealer()
        self.draw_deck = draw_deck
        self.discard_deck = discard_deck


def card_img_lookup(suit: str, val: str) -> pygame.image:
    assert val in CARD_VALS
    assert suit in CARD_SUITS
    img_path = os.path.join("assets", "cards", suit + "_" + val + ".png")
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
    return img


def menu_button_clicked():
    print("menu button clicked!")


def hit_button_clicked():
    print("hit button clicked!")


def stand_button_clicked():
    print("stand button clicked!")


def surrender_button_clicked():
    print("surrender button clicked!")


def split_button_clicked():
    print("split button clicked!")


def double_button_clicked():
    print("double button clicked!")


def draw_popup_menu(window, game_state):
    pass  # TODO


def draw_screen(window, game_state, UI_buttons):
    window.fill(GREEN)
    draw_UI_buttons(window, UI_buttons)
    draw_popup_menu(window, game_state)
    pygame.display.flip()


def handle_UI_button_event(event, UI_buttons):
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        for btn in UI_buttons:
            if btn.mouse_pos_on_button(mouse_pos):
                btn.function()


def handle_event(event, game_state, UI_buttons):
    handle_UI_button_event(event, UI_buttons)

    # TODO: research on implementation of card game design principles and architectures.
    # Use events or a game state class? How should modules talk to each other?

    # After button input: eval the following, unless there is a better way...
    # place bets
    # deal cards # TODO: card move animations and sounds
    # players play
    # dealer plays
    # evaluate hands
    # settle bets


def build_draw_pile(num_decks: int) -> List(Card):
    pile = []
    for _ in range(num_decks):
        for card_val in CARD_VALS:
            for card_suit in CARD_SUITS:
                pile.append(Card(card_suit, card_val))
    random.shuffle(pile)
    return pile


def draw_UI_buttons(window, UI_buttons):
    for btn in UI_buttons:
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


def main():
    pygame.init()
    icon_img = pygame.image.load(os.path.join("assets", "blackjackicon.png"))
    pygame.display.set_icon(icon_img)
    pygame.display.set_caption("mc21 - Blackjack for Humans")
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # TODO: init menu and settings, suggest using draw_popup_menu()

    draw_deck = build_draw_pile(NUM_DECKS_IN_GAME)
    discard_deck = []  # Empty list to hold dead cards before reshuffle.
    player1 = Player()
    human_players = [player1]
    dealer = Dealer()
    game_state = GameState(human_players, dealer, draw_deck, discard_deck)
    UI_buttons = define_UI_buttons()

    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)  # Ensure while loop only executes per FPS timing.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            handle_event(event, game_state, UI_buttons)

        draw_screen(window, game_state, UI_buttons)


if __name__ == "__main__":
    main()
