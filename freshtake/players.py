
from __future__ import annotations
from baseclasses import Call
from cardcollection import CardCollection

class Player():

    def __init__(self):
        self.hand = CardCollection()
        self.split_hand = CardCollection()
        self.wallet = 1000
        self.wager = 2

    def set_wager(self, wager) -> None:
        if type(wager) is not int or type(wager) is not float:
            raise TypeError('wager must be an int or float')
        if wager <= 0:
            raise ValueError('wager must be greater than 0')
        self.wager = wager

    def get_wallet_amount(self):
        return self.wallet

    def get_hand_value(self) -> int:
        return self.hand.get_total_value()

    def get_hand_len(self) -> int:
        return len(self.hand)

    def move_all_cards(self, dest : CardCollection) -> None:
        self.hand.move_all_cards(dest)
        self.split_hand.move_all_cards(dest)

    def __str__(self) -> str:
        return str(self.get_hand_value()) + ' ' + str(self.hand)

    def add_card_to_hand(self, card_value : int) -> None:
        if type(card_value) is not int:
            raise TypeError('card_value must be type int')
        if not (2 <= card_value <= 11):
            raise ValueError('card_value must be between 2 and 11')
        self.hand[card_value] += 1

    def make_call(self, dealer_face_up_card=None, deck=None) -> Call:
        if self.get_hand_value() < 17:
            return Call.HIT
        return Call.STAND


class Dealer():
    def __init__(self, strategy=None):
        self.hand = CardCollection()
        self.strategy = strategy
        self.face_up_card = None
        self.face_down_card = None

    def get_hand_len(self) -> int:
        return len(self.hand)

    def get_hand_value(self) -> int:
        return self.hand.get_total_value()

    def __str__(self) -> str:
        return str(self.get_hand_value()) + ' ' + str(self.hand)

    def add_card_to_hand(self, card_value : int):
        self.hand[card_value] += 1
        if self.get_hand_len() == 1:
            self.face_up_card = card_value
        if self.get_hand_len() == 2:
            self.face_down_card = card_value

    def get_face_up_card(self):
        return self.face_up_card

    def get_face_down_card(self):
        return self.face_down_card

    def make_call(self, dealer_face_up_card=None, deck=None) -> Call:
        if self.get_hand_value() < 17:
            return Call.HIT
        return Call.STAND

    def move_all_cards(self, dest : CardCollection) -> None:
        self.face_up_card, self.face_down_card = None, None
        self.hand.move_all_cards(dest)

