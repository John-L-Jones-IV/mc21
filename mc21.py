#!/usr/bin/env python3
"""
mc21.py
Main running script for Monte Carlo simulations of 21
"""
import random, os, time
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
from blackjack import Card, build_deck, Status, Player, Dealer, UIPlayer
from blackjack import BasicStratPlayer, CCPlayer, HLPlayer, deal_cards
from blackjack import clear_table, print_UI, VALS, SUITS, Status, SimplePlayer

TRIALS = 75
HANDS = 1600

def simulate_trial(num_hands):
    """ returns balence_log array for player1 during simulated number of hands """
    balence_log = []
    used_cards = []
    cards_showing = []
    deck = build_deck

    dealer = Dealer(deck, used_cards, cards_showing)

    # player1 = SimplePlayer(0, deck, used_cards, cards_showing)
    player1 = BasicStratPlayer(0, deck, used_cards, cards_showing, dealer)
    # player1 = HLPlayer(0, deck, used_cards, cards_showing, dealer)

    for _ in range(num_hands):
        deal_cards([dealer, player1])
        balence_log.append(player1.balence)

        # set wager
        player1.set_wager(1)

        # player loop
        while player1.status != Status.STAND:
            player1.move()

        # dealer loop
        while dealer.status != Status.STAND:
            dealer.move()

        # eval hands
        dealer_hand_val = dealer.best_hand_val()
        for player in players:
            # no split
            if len(player.split_hand) == 0:
                p_hand_val = player.best_hand_val()
                if p_hand_val > 21 or p_hand_val <= 0:
                    player.lose()
                elif player.has_blackjack() and not dealer.has_blackjack():
                    player.win(1.5)
                elif not player.has_blackjack() and dealer.has_blackjack():
                    player.lose()
                elif p_hand_val > dealer_hand_val:
                    player.win()
                elif p_hand_val < dealer_hand_val:
                    player.lose()
            # split hands
            else:
                for i in range(2):
                    if i == 1:
                        player.hand = player.split_hand
                        player.set_wager(player.split_wager)
                    p_hand_val = player.best_hand_val()
                    if p_hand_val > 21 or p_hand_val <= 0:
                        player.lose()
                    elif p_hand_val > dealer_hand_val:
                        player.win()
                    elif p_hand_val < dealer_hand_val:
                        player.lose()

        clear_table([dealer]+players)
    return balence_log

def main():
    with Pool() as pool:
        winnings = pool.map(simulate_trial, [HANDS]*TRIALS)
    winnings = np.array(winnings)

    # plot all simulated games
    t = np.arange(0, HANDS)
    for i in range(TRIALS):
        plt.plot(t, winnings[:][i])
    plt.title(str(TRIALS)+' simulated games')
    plt.xlabel('Number of hands played')
    plt.ylabel('Balence')
    t = np.arange(0, HANDS)
    avg = np.mean(winnings, axis=0)
    ci95 = np.std(winnings, axis=0)*1.96 # 95% confidence interval
    plt.plot(t, avg, 'k', t, avg-ci95, 'k--', t, avg+ci95, 'k--')
    plt.xlabel('Number of hands played')
    print('exp return:', str(round((avg[-1]/HANDS*100), 4))+' +/-'
            +str(round((ci95[-1]/HANDS*100), 4))+'%')
    plt.show()

if __name__ == '__main__':
    main()
