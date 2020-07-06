#!/usr/bin/env python3
"""
mc21.py
Main running script for Monte Carlo simulations of 21

John L. Jones IV
"""
import random
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
from blackjack import build_deck, clear_table, deal_cards
from Players import Status, Player, Dealer, SimplePlayer


TRIALS = 75
HANDS = 1600


def simulate_trial(num_hands):
    """
    returns balence_log array for player1 during simulated number of hands
    """
    balence_log = []
    used_cards = []
    cards_showing = []
    deck = build_deck()

    dealer = Dealer(deck, used_cards)

    player1 = SimplePlayer(deck, used_cards)
    # player1 = BasicStratPlayer(0, deck, used_cards, dealer)
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
        p_hand_val = player1.best_hand_val()
        if p_hand_val > 21 or p_hand_val <= 0:
            player1.lose()
        elif player1.has_blackjack() and not dealer.has_blackjack():
            player1.win(1.5)
        elif not player1.has_blackjack() and dealer.has_blackjack():
            player1.lose()
        elif p_hand_val > dealer_hand_val:
            player1.win()
        elif p_hand_val < dealer_hand_val:
            player1.lose()

        clear_table([dealer, player1])
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
    ci95 = np.std(winnings, axis=0)*1.96  # 95% confidence interval
    plt.plot(t, avg, 'k', t, avg-ci95, 'k--', t, avg+ci95, 'k--')
    plt.xlabel('Number of hands played')
    print('exp return:', str(round((avg[-1]/HANDS*100), 4)) + ' +/-'
          + str(round((ci95[-1]/HANDS*100), 4)) + '%')
    plt.show()


if __name__ == '__main__':
    main()
