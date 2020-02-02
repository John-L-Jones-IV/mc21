#!/usr/bin/env python3
import os, random, time, stastics
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from enum import IntEnum

VALS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Q', 'J', 'K']
SUITS = ['Clubs', 'Heart', 'Diamond', 'Spades']

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
    def __str__(self):
        if self.val == 'Blank':
            return 'BLANK'
        if self.suit == 'Clubs':
            suit = '♣'
        elif self.suit == 'Heart':
            suit = '♥'
        elif self.suit == 'Diamond':
            suit = '♦'
        elif self.suit == 'Spades':
            suit = '♠'
        return str(self.val) + ' ' + suit

deck = []
for decks in range(8):
    for val in VALS:
        for suit in SUITS:
            deck.append(Card(suit, val))
random.shuffle(deck)
blank_card = Card('Plastic', 'Blank')
rand_index = 8 + random.randint(-4,4)
deck.insert(rand_index, blank_card)

used_cards = []
cards_showing = []

def reshuffle():
    """ Once the Blank card has been removed from the deck,
    reshuffle combines used cards and remaining cards,
    shuffles, and re-inserts the Blank card """
    deck.extend(used_cards)
    random.shuffle(deck)
    rand_index = 20 + random.randint(-10,10)
    deck.insert(rand_index, blank_card)
    
def hand_val(hand, hard=False):
    """ returns the value of hand
    if hard is true Aces are 1 otherwise Aces are 11 """
    val = 0
    for card in hand:
        if card.val == 'K' or card.val == 'Q' or card.val == 'J':
            val += 10
        elif card.val == 'A' and not hard:
            val += 11
        elif card.val == 'A' and hard:
            val += 1
        else:
            val += int(card.val)
    return val

def best_hand_val(hand):
    """ returns most favorable value of hand """
    if hand_val(hand, hard=True) > 21:
        return 0
    if hand_val(hand) <= 21:
        return hand_val(hand) 
    return hand_val(hand, hard=True)

class Status(IntEnum):
    STAND = 0
    PLAY = 1

class Player(object):
    def __init__(self, balence=0):
        self.hand = []
        self.status = Status.PLAY
        self.balence = balence
        self.wager = 0
    def set_wager(self, wager):
        self.wager = wager
    def hit(self):
        card = deck.pop()
        if card.val is 'Blank':
            reshuffle()
            card = deck.pop()
        self.hand.append(card)
        if not (isinstance(self, Dealer) and len(self.hand) == 2):
            cards_showing.append(card)
        if (hand_val(self.hand, hard=True) >= 21 or
                best_hand_val(self.hand) == 21 ):
            self.status = Status.STAND
    def win(self):
        self.balence += self.wager
    def lose(self):
        self.balence -= self.wager
    def disp_hand(self):
        for card in self.hand:
            print(card)
    def move(self):
        """ Implemented in child classes only """
        raise NotImplementedError

class Dealer(Player):
    def __init__(self):
        self.hand = []
        self.status = Status.PLAY
    def move(self):
        if best_hand_val(self.hand) >= 17 or best_hand_val(self.hand) == 0:
            self.status = Status.STAND
        else:
            self.hit()

class UIPlayer(Player):
    def __init__(self, balence):
        super().__init__(balence)
    def move(self):
        s = input('S to stand, H to hit: ').lower()
        if s == 's':
            self.status = Status.STAND
        elif s == 'h':
            self.hit()
        else:
            print('Must enter S or H')

class SimplePlayer(Player):
    def __init__(self, balence):
        super().__init__(balence)
    def move(self):
        if best_hand_val(self.hand) >= 17 or best_hand_val(self.hand) == 0:
            self.status = Status.STAND
        elif self.balence >= 0:
            self.hit()

def deal_cards(players):
    for i in range(2):
        for player in players:
            player.hit()

def clear_table(players):
    cards_showing = []
    for player in players:
        player.status = Status.PLAY
        while len(player.hand):
            used_cards.append(player.hand.pop())

def print_UI(dealer, player1, dealer_move=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    # for card in deck:
    #     print(card)
    print('Balence:', player1.balence)
    print('Wager:', player1.wager, '\n')
    if dealer_move:
        print('Dealer showing:', best_hand_val(dealer.hand))
        dealer.disp_hand()
        print()
    else:
        print('Dealer showing:\n'+str(dealer.hand[0]), '\n')
    print('Your hand:', best_hand_val(player1.hand))
    player1.disp_hand()

def UImain():
    player1 = UIPlayer(200)
    dealer = Dealer()
    while player1.balence > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Balence:', player1.balence)
        s = int(input('Place wager amount: '))
        player1.set_wager(s)
        deal_cards([dealer, player1])

        # UI player loop
        if isinstance(player1, UIPlayer):
            while (player1.status != Status.STAND):
                print_UI(dealer, player1)
                player1.move()

        while dealer.status != Status.STAND:
            print_UI(dealer, player1, dealer_move=True)
            dealer.move()
            time.sleep(1)
        print_UI(dealer, player1, dealer_move=True)

        dealer_hand_val = best_hand_val(dealer.hand)
        player1_hand_val = best_hand_val(player1.hand)
        if dealer_hand_val > player1_hand_val:
            print('You lose', player1.wager)
            player1.balence -= player1.wager
        if dealer_hand_val < player1_hand_val:
            print('You win', player1.wager)
            player1.balence += player1.wager
        input('\nhit any key to continue ')
        clear_table([dealer, player1])

def main():
    TRIALS = 1000
    HANDS = 250
    winnings = np.empty([TRIALS, HANDS])
    for i in range(TRIALS):
        player1 = SimplePlayer(200)
        dealer = Dealer()
        players = [player1]
        for j in range(HANDS): # hands
            deal_cards([dealer] + players)
            # print('Trial:', i, '\tHand:', j)

            winnings[i, j] = player1.balence

            # set wager
            for player in players:
                player.set_wager(5)

            # player loop
            while sum([player.status for player in players]):
                for player in players:
                    if player.status == Status.STAND:
                        continue
                    player.move()

            # dealer loop
            while dealer.status != Status.STAND:
                dealer.move()

            # eval hands
            dealer_hand_val = best_hand_val(dealer.hand)
            for player in players:
                if player.balence <= 0:
                    continue
                player_hand_val = best_hand_val(player.hand)
                if player_hand_val > dealer_hand_val and player_hand_val <= 21:
                    player.lose()
                if player_hand_val < dealer_hand_val and dealer_hand_val <= 21:
                    player.lose()
            clear_table([dealer]+players)

    # plot results
    t = np.arange(0, HANDS)
    fig, ax = plt.subplots()
    for i in range(TRIALS):
        ax.plot(t, winnings[:][i])
    plt.show()

    t = np.arange(0, HANDS)
    fig, ax = plt.subplots()
    for i in range(HANDS):
        pass


if __name__ == '__main__':
    main()
