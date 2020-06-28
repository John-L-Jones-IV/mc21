#!/usr/bin/env python3
"""
UIblackjack.py
A User Interface game of blackjack, used to test simulation environment and
play blackjack for fun.

relies on blackjack.py

John L. Jones IV
"""
from blackjack import Card, Player, Dealer, Status, deal_cards, clear_table
from blackjack import print_UI, build_deck
from time import sleep
import os

# Initialize
game_over = False
deck = build_deck()
used_cards = []
p1 = Player(deck, used_cards)
dealer = Dealer(deck, used_cards)
players = [p1, dealer]


def get_wager():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Balence:', p1.balence)
    print('Wager:', p1.wager, '\n')
    str_out = 'Please place your bet. Enter any integer greater than 0.\n'
    while True:
        try:
            wager = int(input(str_out))
            if wager > 0:
                p1.set_wager(wager)
                break
        except ValueError:
            pass


def p1_move():
    while 0 < p1.best_hand_val() < 21 and p1.status > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Balence:', p1.balence)
        print('Wager:', p1.wager)
        print('Dealer showing:', dealer.hand[0], '\n')
        print('Value of hand', p1.best_hand_val())
        print('Cards in hand:')
        p1.disp_hand()
        try:
            move = input("'H' to hit, 'S' to stand\n").upper()
        except ValueError:
            pass
        if move == 'H':
            p1.hit()
        elif move == 'S':
            p1.stand()


def dealer_move():
    while dealer.status > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Balence:', p1.balence)
        print('Wager:', p1.wager)
        dealer.move()
        print('Dealer showing:', dealer.best_hand_val())
        dealer.disp_hand()
        print()
        print('Value of hand', p1.best_hand_val())
        print('Cards in hand:')
        p1.disp_hand()
        sleep(1)

def eval_hands():
    if p1.has_blackjack():
        p1.win(1.5)
        print('Blackjack! You win.')
    elif p1.best_hand_val() > dealer.best_hand_val():
        p1.win()
        print('You win.')
    elif p1.best_hand_val() == dealer.best_hand_val():
        print('Draw.')
    else:
        p1.lose()
        print('You lose.')
    sleep(1)

while not game_over:
    get_wager()
    deal_cards([p1, dealer])
    p1_move()
    dealer_move()
    eval_hands()
    clear_table([p1, dealer])
