#!/usr/bin/env python3
from __future__ import annotations
import copy
import inspect
import os
import sys

import pygame

from model.blackjackcore import MAX_SPLITS, MIN_BET
from view.buttonclickedfunctions import (
    menu_button_clicked,
    hit_button_clicked,
    stand_button_clicked,
    surrender_button_clicked,
    split_button_clicked,
    double_button_clicked,
    deal_button_clicked,
    bet_increase5_clicked,
    bet_decrease5_clicked
)
from view.GUIbutton import UIButton

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

# modlue level persistent variables
_icon_img, window = None, None
play_decission_buttons, bet_buttons, menu_buttons = None, None, None
_previous_game = None  # used to monitor state and trigger animations.
temp_bet = MIN_BET

def init():
    pygame.init()
    global _icon_img, window, play_decission_buttons, bet_buttons, menu_buttons
    _icon_img = pygame.image.load(os.path.join("assets", "blackjackicon.png"))
    pygame.display.set_icon(_icon_img)
    pygame.display.set_caption("mc21 - Blackjack for Humans")
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    play_decission_buttons = define_UI_buttons()
    bet_buttons = define_bet_buttons()
    menu_buttons = define_menu_buttons()

def update_screen(game):
    """Draw GUI screen with pygame."""
    monitor_changes_and_queue_animations(game)
    window.fill(GREEN)

    update_buttons_active_status(game)
    bet_state = len(game.player1.hand) == 0
    if bet_state:
        draw_bet_menu(game)
        # place bet sub menu
        pass
    else:
        draw_players_hands(game.player1.hands)
        draw_dealers_hand(game.dealer.hand)
        draw_game_info(game)
        # TODO: add shade to cards that are not active while drawing
        # draw_active_hand_indicator(game.player1.active_hand_index)
    draw_bankroll(game)
    pygame.display.flip()

def draw_bet_menu(game):
    menu_rect = pygame.Rect((328, 110), (625, 500))
    pygame.draw.rect(window, BLUE, menu_rect, border_radius=10)
    # draw_chip(surface, color, pos, radius, text):
    draw_chip(window, RED, (453, 360), 25, "5")
    draw_chip(window, BLUE, (578, 360), 25, "10")
    draw_chip(window, GREEN, (703, 360), 25, "25")
    draw_chip(window, BLACK, (828, 360), 25, "100")
    x, y = 640, 250
    text_img = FONT.render(f"bet: {temp_bet}", False, WHITE)
    img_width, img_height = text_img.get_size()
    window.blit(text_img, (x - img_width // 2, y - img_height // 2))
    
def change_bet(x):
    global temp_bet
    temp_bet += x
    if temp_bet < MIN_BET:
        bet_buttons["deal"].set_active(False) 
    else:
        bet_buttons["deal"].set_active(True) 
    

#region Controller
def process_user_input(game: Game):
    """Handle pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        handle_event(event, game)

def handle_event(event: pygame.event, game: Game):
    """Handle pygame events and send user request to blackjackcore."""
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos = pygame.mouse.get_pos()
        btns = {}
        btns.update(play_decission_buttons)
        btns.update(bet_buttons)
        for btn in btns.values():
            if btn.is_mouse_position_colliding(mouse_pos):
                btn.function(game)
#end region

def monitor_changes_and_queue_animations(game):
    global _previous_game
    if _previous_game is None:
        _previous_game = copy.deepcopy(game)
        return
    diff_d = get_diffs(_previous_game, game)
    game_change_animations(game, _previous_game, diff_d)
    _previous_game = copy.deepcopy(game)

def game_change_animations(game, prev_game, diff_d):
    if len(diff_d) > 0:
        print('gamestate change detected!')
        print(diff_d)
        print([str(x) for x in diff_d.values()])
    if len(game.deck) < len(prev_game.deck):
        print('card moved from deck')
    if len(game.discard_pile) > len(prev_game.discard_pile):
        print('cards moved to discard pile')
    if game.player1.bankroll != prev_game.player1.bankroll:
        print('player bankroll has changed')

def get_diffs(prev_obj, current_obj):
    # TODO this nessisary? why not just do direct comparisons for triggers?
    if prev_obj is None:
        return current_obj.__dict__

    assert isinstance(current_obj, type(prev_obj))
    cur_d = current_obj.__dict__
    prv_d = prev_obj.__dict__
    return {k: cur_d[k] for k in cur_d if cur_d[k] != prv_d[k]}


def update_buttons_active_status(game):
    if len(game.player1.hand) >= 2:
        update_play_state_buttons_activation_status(game)
    elif len(game.player1.hand) == 0:
        update_bet_state_buttons_activation_status(game)
    all_btns = {}
    all_btns.update(play_decission_buttons)
    all_btns.update(bet_buttons)
    all_btns.update(menu_buttons)
    draw_buttons(all_btns)

def update_bet_state_buttons_activation_status(game):
    for b in play_decission_buttons.values():
        b.set_hidden(True)
    for b in bet_buttons.values():
        b.set_active(True)

def update_play_state_buttons_activation_status(game):
    player = game.player1
    hand = player.hand
    num_hands = len(player.hands)
    hand_len = len(hand)
    btns = play_decission_buttons

    # hit always active in play state
    btns["hit"].set_active(True)

    # stand always active in play state
    btns["stand"].set_active(True)

    is_surrender_btn_active = hand_len == 2 and num_hands == 1
    btns["surrender"].set_active(is_surrender_btn_active)

    is_double_btn_active = hand_len = 2
    btns["double"].set_active(is_double_btn_active)

    try:
        is_split_btn_active = (
            hand_len == 2
            and num_hands <= MAX_SPLITS
            and hand[0].int_value == hand[1].int_value
        )
    except IndexError:
        is_split_btn_active = False
    btns["split"].set_active(is_split_btn_active)


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
        window: pygame.Surface, card: blackjackcore.Card, pos: (x, y)) -> None:
    suit, val = card.suit, card.value
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

def draw_bankroll(game):
    text = f"Bankroll: {game.player1.bankroll}"
    text_surface = FONT.render(text, True, BLACK)
    window.blit(text_surface, (20, 20))

def draw_game_info(game):
    x_start, y = 250, 690
    x_offset = HAND_STEP * game.player1.active_hand_index
    x = x_start + x_offset
    best_hand_value = game.player1.hand.best_value
    second_best_hand_value = game.player1.hand.second_best_value

    if best_hand_value != second_best_hand_value and best_hand_value <= 21:
        game_info_str = f"{second_best_hand_value}/{best_hand_value}"
    else:
        game_info_str = str(best_hand_value)
    text_surface = FONT.render(game_info_str, True, BLACK)
    window.blit(text_surface, (x, y))

def define_bet_buttons():
    bet_increase5_btn = UIButton((20, 600, 100, 25), "+5", bet_increase5_clicked)
    bet_decrease5_btn = UIButton((20, 675, 100, 25), "-5", bet_decrease5_clicked)
    deal_btn = UIButton((20, 500, 100, 25), "Deal", deal_button_clicked)
    return {
            "bet_increase5": bet_increase5_btn,
            "bet_decrease5": bet_decrease5_btn,
            "deal": deal_btn
    }


def define_menu_buttons():
    menu_btn = UIButton((20, 155, 100, 25), "Menu", menu_button_clicked)
    return {
            "menu": menu_btn
    }

def define_UI_buttons():
    hit_btn = UIButton((20, 675, 100, 25), "Hit", hit_button_clicked)
    stand_btn = UIButton((20, 640, 100, 25), "Stand", stand_button_clicked)
    double_btn = UIButton((20, 605, 100, 25), "Double", double_button_clicked)
    split_btn = UIButton((20, 535, 100, 25), "Split", split_button_clicked)
    surrender_btn = UIButton((20, 570, 100, 25), "Surrender", surrender_button_clicked)

    return {
        "hit": hit_btn,
        "stand": stand_btn,
        "double": double_btn,
        "split": split_btn,
        "surrender": surrender_btn,
    }


if __name__ == "__main__":
    main()
