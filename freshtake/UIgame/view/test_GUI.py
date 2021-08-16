#!/usr/bin/env python3
import copy
import random
import unittest

from model.blackjackcore import Game
from view.GUI import get_diffs


class A:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TestHelperFunctions(unittest.TestCase):
    def test_get_objs_diffs(self):
        a1 = None
        a2 = A(3, [1, 2, 3])
        self.assertEqual(get_diffs(a1, a2), {"x": 3, "y": [1, 2, 3]})

        game1 = Game()
        game2 = copy.deepcopy(game1)
        self.assertEqual(get_diffs(game1, game2), {})

        game1 = None
        game2 = Game()
        diffs = get_diffs(game1, game2)
        keys = [
            "deck",
            "discard_pile",
            "dealer",
            "state",
            "player1",
            "players",
            "active_player_index",
        ]
        for key in keys:
            self.assertIn(key, diffs)
        self.assertEqual(len(diffs), 7)

        game1 = Game()
        game2 = copy.deepcopy(game1)
        game2.deal_cards()
        diffs = get_diffs(game1, game2)
        keys = ["deck", "dealer", "player1", "players"]
        for key in keys:
            self.assertIn(key, diffs)
        self.assertEqual(len(diffs), 4)
