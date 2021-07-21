#!/usr/bin/env python3
"""
main.py
Runs Monte Carlo Simulations of 21 card game.

John L. Jones IV
"""
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np

import game

NUM_HANDS_TO_PLAY = 1200
NUM_SIMULATIONS = 25
NUM_PROCESSES = 6   # Processes for multithreading

def plot(matrix):
    matrix = np.array(matrix)
    t = np.arange(NUM_HANDS_TO_PLAY)
    cash_t = np.array(matrix)
    for sim in range(NUM_SIMULATIONS):
        plt.plot(t, cash_t[sim])
    plt.show()

def main():
    with multiprocessing.Pool(NUM_PROCESSES) as p:
        result = p.map(game.simulate, [NUM_HANDS_TO_PLAY]*NUM_SIMULATIONS)
    plot(result)

if __name__ == '__main__':
    main()

