#!/usr/bin/env python3
import unittest

from model.classes import Card, Hand


class TestCardMethods(unittest.TestCase):
    def test_get_val_as_int(self):
        card = Card("hearts", "A")
        self.assertEqual(card.get_value_as_int(), 11)
        card = Card("spades", "A")
        self.assertEqual(card.get_value_as_int(), 11)
        card = Card("clubs", "A")
        self.assertEqual(card.get_value_as_int(), 11)
        card = Card("diamonds", "A")
        self.assertEqual(card.get_value_as_int(), 11)
        
        card = Card("hearts", "J")
        self.assertEqual(card.get_value_as_int(), 10)
        card = Card("clubs", "Q")
        self.assertEqual(card.get_value_as_int(), 10)
        card = Card("hearts", "K")
        self.assertEqual(card.get_value_as_int(), 10)
        card = Card("spades", "J")
        self.assertEqual(card.get_value_as_int(), 10)

        card = Card("hearts", "10")
        self.assertEqual(card.get_value_as_int(), 10)
        card = Card("spades", "6")
        self.assertEqual(card.get_value_as_int(), 6)
        card = Card("clubs", "2")
        self.assertEqual(card.get_value_as_int(), 2)
        card = Card("diamonds", "2")
        self.assertEqual(card.get_value_as_int(), 2)
        

    def test_get_value_as_str(self):
        card = Card("hearts", "A")
        self.assertEqual(card.get_value_as_str(), "A")
        card = Card("spades", "A")
        self.assertEqual(card.get_value_as_str(), "A")
        card = Card("clubs", "A")
        self.assertEqual(card.get_value_as_str(), "A")
        card = Card("diamonds", "A")
        self.assertEqual(card.get_value_as_str(), "A")
        
        card = Card("hearts", "J")
        self.assertEqual(card.get_value_as_str(), "J")
        card = Card("clubs", "Q")
        self.assertEqual(card.get_value_as_str(), "Q")
        card = Card("hearts", "K")
        self.assertEqual(card.get_value_as_str(), "K")
        card = Card("spades", "J")
        self.assertEqual(card.get_value_as_str(), "J")

        card = Card("hearts", "10")
        self.assertEqual(card.get_value_as_str(), "10")
        card = Card("spades", "6")
        self.assertEqual(card.get_value_as_str(), "6")
        card = Card("clubs", "2")
        self.assertEqual(card.get_value_as_str(), "2")
        card = Card("diamonds", "2")
        self.assertEqual(card.get_value_as_str(), "2")

class TestHandMethods(unittest.TestCase):
    def test_get_best_hand_value(self):
        hand = Hand()
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "10"))
        self.assertEqual(hand.get_best_value(), 21)




