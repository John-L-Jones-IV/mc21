#!/usr/bin/env python3
from __future__ import annotations

class CardCollection():

    def __init__(self) -> None:
        self._cards = dict()
        for card in range(2, 12):
            self._cards[card] = 0

    def __eq__(self, other: CardCollection) -> bool:
        if type(other) is not CardCollection:
            raise TypeError('CardCollection type can only be compared to other CardCollecion type')
        return self._cards == other._cards

    def __iter__(self):
        return self._cards.__iter__()

    def __repr__(self):
        return str(self._cards)

    def _check_key_request(self, k):
        if k not in range(2,12):
            raise ValueError('CardCollection Type only holds values 2 thru 11')
        if type(k) is not int:
            raise TypeError('CardCollection only has int keys')

    def __getitem__(self, k):
        self._check_key_request(k)
        return self._cards.__getitem__(k)

    def get(self, k):
        self._check_key_request(k)
        return self._cards.get(k)

    def __setitem__(self, k, v):
        self._check_key_request(k)
        self._cards.__setitem__(k, v)

    def get_num_cards(self) -> int:
        return sum([self._cards.get(key) for key in self._cards])

    def __len__(self) -> int:
        return self.get_num_cards()

    def move_all_cards(self, other_cards : CardCollection) -> None:
        for card in self._cards:
            other_cards[card] += self._cards.get(card)
            self._cards[card] = 0

    def _get_aceis11_total(self):
        return sum([self._cards.get(key)*key for key in self._cards])

    def _get_aceis1_total(self):
        hard_toal = 0
        for key in self._cards:
            if key != 11:
                hard_toal += key*self._cards.get(key)
            elif key == 11:
                hard_toal += self._cards.get(key)
        return hard_toal

    def get_total_value(self):
        if self._get_aceis11_total() <= 21:
            return self._get_aceis11_total()
        return self._get_aceis1_total()

