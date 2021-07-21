#!/usr/bin/env python3
import random

from baseclasses import Call, SplitsAllowed
from cardcollection import CardCollection
from deck import Deck
from players import Player, Dealer

DEALER_HITS_ON_SOFT17 = True
CAN_PLAYER_DOUBLE_AFTER_SPLITTING = True
IS_SURRENDER_ALLOWED = True
SPLITS_ALLOWED = 1
NUM_DECKS = 6
BLACKJACK_ODDS = 3.0/2.0

MIN_BET = 2
MAX_BET = 500
CUT_MIN = 60
CUT_MAX = 75

def play_round(player, cut_ptr, draw_pile, discard_pile):
    if player is type(Player):
        player.set_wager()
    player_call = player.make_call()
    split_used = False
    while(player_call != Call.STAND and player.get_hand_value() <= 21):
        if len(draw_pile) <= cut_ptr[0]:
            discard_pile.move_all_cards(draw_pile.cards)
            cut_ptr[0] = random.randint(CUT_MIN, CUT_MAX)
        if player_call == Call.SPLIT and not split_used:
            player.split_hand, player.hand = player.hand, player.split_hand
            play_round(player, cut_ptr, draw_pile, discard_pile)
            player.split_hand, player.hand = player.hand, player.split_hand
            split_used = True
        if player_call == Call.SURRENDER:
            player.set_wager(player.get_wager() * 0.5)
            player.move_all_card(discard_pile)
        elif player_call == Call.DOUBLE:
            player.add_card_to_hand(draw_pile.pop_a_card())
            player.set_wager(player.get_wager() * 2)
            break
        elif player_call == Call.HIT:
            player.add_card_to_hand(draw_pile.pop_a_card())
            player_call = player.make_call()

def hand_beats_dealers_hand(hand, dealer_hand) -> bool:
    return player_val > dealer_val and player_val <= 21

def handle_split_eval(player, dealer):
    player_win = hand_beats_dealer_hand(player.split_hand, dealer.hand)
    pass

def evaluate_round(player, dealer):
    if len(player.split_hand) != 0:
        tmp = CardCollection()
        player.split_hand.move_all_cards(tmp)
        #FIXME:
        #evaluate_round(player, dealer)
        print('FIXME: split hands')
    player_val = player.get_hand_value()
    dealer_val = dealer.get_hand_value()
    player_win = dealer_val < player_val <= 21
    if player_val == 21 and len(player.hand) == 2 and player_win:
        player.wallet += player.wager * BLACKJACK_ODDS
    elif not player_win:
        player.wallet -= player.wager


def clear_table(list_of_players_with_dealer, discard_pile):
    for p in list_of_players_with_dealer:
        p.move_all_cards(discard_pile)


def simulate(numHands):
    card_cut_ptr = [random.randint(CUT_MIN, CUT_MAX)]
    draw_pile = Deck(NUM_DECKS)
    discard_pile = CardCollection()
    dealer = Dealer()
    player1 = Player()
    players = [player1]
    log = []

    for _ in range(numHands):

        # deal cards
        for _ in range(2):
            for p in players + [dealer]:
                p.add_card_to_hand(draw_pile.pop_a_card())

        for p in players + [dealer]:
            play_round(p, card_cut_ptr, draw_pile, discard_pile)

        for p in players:
            evaluate_round(p, dealer)

        log.append(p.wallet)

        clear_table(players + [dealer], discard_pile)

    return log

