#!/usr/bin/env python3
import unittest
from collections import Counter

from deck import Deck

class TestDeskMethods(unittest.TestCase):

    def test_pop_a_card(self):
        dk = Deck(1)
        for i in range(52, 0, -1):
            self.assertGreaterEqual(dk.pop_a_card(), 2)
            self.assertLessEqual(dk.pop_a_card(), 11)

    def test_get_num_cards(self):
        dk = Deck(1)
        self.assertEqual(dk.get_num_cards(), 52)
        self.assertEqual(Deck(2).get_num_cards(), 104)
        dk.pop_a_card()
        self.assertEqual(dk.get_num_cards(), 51);
        dk.pop_a_card()
        self.assertEqual(dk.get_num_cards(), 50);

    def test__len__(self):
        dk = Deck(1)
        self.assertEqual(len(dk), 52)
        self.assertEqual(len(Deck(2)), 104)
        dk.pop_a_card()
        self.assertEqual(len(dk), 51);
        dk.pop_a_card()
        self.assertEqual(len(dk), 50);

    def test_get_card_weights(self):
        dk = Deck(1)
        self.assertEqual(dk.get_card_weights(), [4]*8+[16]+[4])
        dk = Deck(0)
        self.assertEqual(dk.get_card_weights(), [0]*10)
        dk = Deck(2)
        self.assertEqual(dk.get_card_weights(), [8]*8+[32]+[8])

    def test_get_card_probabilities(self):
        dk = Deck(1)
        expected_list = [4.0/52]*8+[16.0/52]+[4.0/52]
        self.assertEqual(dk.get_card_probabilities(), expected_list)
        dk = Deck(2)
        self.assertEqual(dk.get_card_probabilities(), expected_list)
    
    @unittest.expectedFailure
    def test_get_card_probabilities_with_no_cards(self):
        dk = Deck(0)
        self.assertRaises(Exception, dk.get_card_probabilities())

    def test_pop_a_card(self):
        l = []
        dk = Deck(1)
        for i in range(51, -1, -1):
            l.append(dk.pop_a_card())
            self.assertEqual(len(dk), i)
        d = Counter(l)
        for i in range(2, 10):
            self.assertEqual(4, d[i])
        self.assertEqual(16, d[10])
        self.assertEqual(4, d[11])

    @unittest.expectedFailure
    def test_pop_a_card_with_empty_deck(self):
        dk = Deck(1)
        for _ in range(52):
            dk.pop_a_card()
        self.assertRaises(Exception, dk.pop_a_card())

if __name__ == '__main__':
    unittest.main()

