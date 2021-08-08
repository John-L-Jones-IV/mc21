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
    def test_get_best_value(self):
        hand = Hand()
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "10"))
        self.assertEqual(hand.get_best_value(), 21)

        hand = Hand()
        hand.add_card(Card("clubs", "K"))
        hand.add_card(Card("clubs", "10"))
        self.assertEqual(hand.get_best_value(), 20)

        hand = Hand()
        hand.add_card(Card("clubs", "K"))
        hand.add_card(Card("clubs", "10"))
        hand.add_card(Card("clubs", "J"))
        self.assertEqual(hand.get_best_value(), 30)

        hand = Hand()
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "10"))
        hand.add_card(Card("clubs", "J"))
        self.assertEqual(hand.get_best_value(), 21)

        hand = Hand()
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "9"))
        self.assertEqual(hand.get_best_value(), 21)

        hand = Hand()
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "A"))
        self.assertEqual(hand.get_best_value(), 13)

        hand = Hand()
        hand.add_card(Card("clubs", "2"))
        hand.add_card(Card("clubs", "3"))
        self.assertEqual(hand.get_best_value(), 5)

    def test_get_second_best_value(self):
        hand = Hand()
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "10"))
        self.assertEqual(hand.get_second_best_value(), 11)

        hand = Hand()
        hand.add_card(Card("clubs", "K"))
        hand.add_card(Card("clubs", "10"))
        self.assertEqual(hand.get_second_best_value(), 20)

        hand = Hand()
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "A"))
        hand.add_card(Card("clubs", "A"))
        self.assertEqual(hand.get_second_best_value(), 3)



    def test_is_blackjack(self):
        hand = Hand()
        hand.add_card(Card("spades", "K"))
        hand.add_card(Card("hearts", "A"))
        self.assertTrue(hand.is_blackjack())

        hand = Hand()
        hand.add_card(Card("spades", "Q"))
        hand.add_card(Card("hearts", "A"))
        self.assertTrue(hand.is_blackjack())

        hand = Hand()
        hand.add_card(Card("spades", "Q"))
        hand.add_card(Card("hearts", "5"))
        hand.add_card(Card("diamonds", "6"))
        self.assertFalse(hand.is_blackjack())

        hand = Hand()
        hand.add_card(Card("spades", "Q"))
        hand.add_card(Card("hearts", "6"))
        hand.add_card(Card("diamonds", "6"))
        self.assertFalse(hand.is_blackjack())

        hand = Hand()
        hand.add_card(Card("spades", "Q"))
        hand.add_card(Card("clubs", "10"))
        self.assertFalse(hand.is_blackjack())

        hand = Hand()
        hand.add_card(Card("spades", "2"))
        hand.add_card(Card("hearts", "2"))
        self.assertFalse(hand.is_blackjack())

    def test_is_bust(self):
        hand = Hand()
        hand.add_card(Card("spades", "K"))
        hand.add_card(Card("hearts", "A"))
        self.assertFalse(hand.is_bust())

        hand = Hand()
        hand.add_card(Card("spades", "10"))
        hand.add_card(Card("hearts", "A"))
        self.assertFalse(hand.is_bust())

        hand = Hand()
        hand.add_card(Card("spades", "K"))
        hand.add_card(Card("hearts", "Q"))
        self.assertFalse(hand.is_bust())

        hand = Hand()
        hand.add_card(Card("spades", "A"))
        hand.add_card(Card("clubs", "3"))
        hand.add_card(Card("hearts", "10"))
        self.assertFalse(hand.is_bust())

        hand = Hand()
        for i in range(21):
            hand.add_card(Card("spades", "A"))
        self.assertFalse(hand.is_bust())

        hand = Hand()
        hand.add_card(Card("spades", "7"))
        hand.add_card(Card("hearts", "7"))
        hand.add_card(Card("clubs", "8"))
        self.assertTrue(hand.is_bust())

        hand = Hand()
        hand.add_card(Card("spades", "2"))
        hand.add_card(Card("hearts", "7"))
        hand.add_card(Card("clubs", "5"))
        hand.add_card(Card("clubs", "K"))
        self.assertTrue(hand.is_bust())

class TestPlayerMethods(unittest.TestCase):
    def test_split_hand(self):
        player = Player(200)
