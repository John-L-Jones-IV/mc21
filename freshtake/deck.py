#!/usr/bin/env python3
from __future__ import annotations

import random

from cardcollection import CardCollection

class Deck():

    def __init__(self, num_decks : int):
        self.cards = CardCollection()
        for value in range(2, 10):          # 1-9 cards
            self.cards[value] = 4*num_decks
        self.cards[10] = 16*num_decks       # 10, Q, K, J
        self.cards[11] = 4*num_decks        # A

    def __repr__(self) -> str:
        return str(self.cards)

    def get_num_cards(self) -> int:
        return self.cards.get_num_cards()

    def __len__(self) -> int:
        return self.get_num_cards()

    def get_card_weights(self) -> List[int]:
        return [self.cards.get(key) for key in self.cards]

    def get_card_probabilities(self) -> List[float]:
        length = float(self.get_num_cards())
        if length <= 0:
            raise Exception('No Cards in Deck')
        return [float(i)/length for i in self.get_card_weights()]

    def pop_a_card(self) -> int:
        """
        Model removing the top card from the deck and returning the card value.
        """
        if self.get_num_cards() <= 0:
            raise Exception('Can not pop card. Card deck has no cards.')
        w = self.get_card_weights()
        card_key = int(random.choices(list(self.cards), weights=w)[0])
        self.cards[card_key] -= 1
        return card_key

