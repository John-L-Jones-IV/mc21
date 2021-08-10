#!/usr/bin/env python3
import unittest
import random

from model.blackjackcore import Card, Hand, Player, Deck, Dealer

SUITS = ["hearts", "spades", "diamonds", "clubs"]


def get_random_suit():
    return random.choice(SUITS)


randomsuit = get_random_suit()


class TestHelperFunctions(unittest.TestCase):
    def test_get_random_suit(self):
        for i in range(28):
            self.assertIn(randomsuit, SUITS)


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
    def test_get_best_hand_value(self):
        player = Player(200)
        player.add_card_to_hand(Card("hearts", "5"))
        player.add_card_to_hand(Card("clubs", "6"))
        self.assertEqual(player.get_best_hand_value(), 11)

        player = Player(200)
        player.add_card_to_hand(Card("hearts", "6"))
        player.add_card_to_hand(Card("clubs", "6"))
        self.assertEqual(player.get_best_hand_value(), 12)

        player = Player(200)
        player.add_card_to_hand(Card("hearts", "A"))
        player.add_card_to_hand(Card("clubs", "A"))
        self.assertEqual(player.get_best_hand_value(), 12)

        player = Player(200)
        player.add_card_to_hand(Card("hearts", "A"))
        player.add_card_to_hand(Card("clubs", "A"))
        player.add_card_to_hand(Card("spades", "A"))
        self.assertEqual(player.get_best_hand_value(), 13)

        player = Player(200)
        player.add_card_to_hand(Card("hearts", "A"))
        player.add_card_to_hand(Card("clubs", "K"))
        self.assertEqual(player.get_best_hand_value(), 21)

    def test_get_second_best_hand_value(self):
        player = Player(200)
        player.add_card_to_hand(Card("hearts", "A"))
        player.add_card_to_hand(Card("clubs", "K"))
        self.assertEqual(player.get_second_best_hand_value(), 11)

        player = Player(200)
        player.add_card_to_hand(Card("hearts", "A"))
        player.add_card_to_hand(Card("clubs", "7"))
        player.add_card_to_hand(Card("clubs", "7"))
        self.assertEqual(player.get_second_best_hand_value(), 15)

        player = Player(200)
        player.add_card_to_hand(Card("hearts", "2"))
        player.add_card_to_hand(Card("clubs", "2"))
        self.assertEqual(player.get_second_best_hand_value(), 4)

    def test_is_hand_blackjack(self):
        player = Player(200)
        player.add_card_to_hand(Card("hearts", "A"))
        player.add_card_to_hand(Card("clubs", "K"))
        self.assertTrue(player.is_hand_blackjack())

        player = Player(200)
        player.add_card_to_hand(Card("hearts", "A"))
        player.add_card_to_hand(Card("clubs", "10"))
        self.assertTrue(player.is_hand_blackjack())

        player = Player(200)
        player.add_card_to_hand(Card("hearts", "A"))
        player.add_card_to_hand(Card("clubs", "Q"))
        self.assertTrue(player.is_hand_blackjack())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "A"))
        player.add_card_to_hand(Card(randomsuit, "J"))
        self.assertTrue(player.is_hand_blackjack())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "A"))
        player.add_card_to_hand(Card(randomsuit, "5"))
        player.add_card_to_hand(Card(randomsuit, "5"))
        self.assertFalse(player.is_hand_blackjack())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "3"))
        player.add_card_to_hand(Card(randomsuit, "8"))
        player.add_card_to_hand(Card(randomsuit, "4"))
        self.assertFalse(player.is_hand_blackjack())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "10"))
        player.add_card_to_hand(Card(randomsuit, "3"))
        player.add_card_to_hand(Card(randomsuit, "K"))
        self.assertFalse(player.is_hand_blackjack())

    def test_is_hand_bust(self):
        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "5"))
        player.add_card_to_hand(Card(randomsuit, "5"))
        player.add_card_to_hand(Card(randomsuit, "5"))
        player.add_card_to_hand(Card(randomsuit, "8"))
        self.assertTrue(player.is_hand_bust())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "5"))
        player.add_card_to_hand(Card(randomsuit, "5"))
        player.add_card_to_hand(Card(randomsuit, "5"))
        player.add_card_to_hand(Card(randomsuit, "9"))
        self.assertTrue(player.is_hand_bust())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "5"))
        player.add_card_to_hand(Card(randomsuit, "10"))
        player.add_card_to_hand(Card(randomsuit, "9"))
        self.assertTrue(player.is_hand_bust())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "10"))
        player.add_card_to_hand(Card(randomsuit, "A"))
        self.assertFalse(player.is_hand_bust())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "A"))
        player.add_card_to_hand(Card(randomsuit, "J"))
        self.assertFalse(player.is_hand_bust())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "2"))
        player.add_card_to_hand(Card(randomsuit, "2"))
        self.assertFalse(player.is_hand_bust())

        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "2"))
        player.add_card_to_hand(Card(randomsuit, "10"))
        player.add_card_to_hand(Card(randomsuit, "J"))
        self.assertTrue(player.is_hand_bust())

    def test_split_hand(self):
        player = Player(200)
        player.add_card_to_hand(Card(randomsuit, "A"))
        player.add_card_to_hand(Card(randomsuit, "A"))
        card1 = Card("hearts", "10")
        card2 = Card("hearts", "10")
        player.split_hand(card1, card2)
        self.assertEqual(len(player.hands), 2)
        self.assertEqual(player.get_active_hand_index(), 1)
        self.assertTrue(player.is_hand_blackjack())


class TestDeckMethods(unittest.TestCase):
    def test_pop(self):
        deck = Deck(1)
        self.assertEqual(len(deck), 52)
        card = deck.pop()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(deck), 51)

    def test_deal_cards(self):
        deck = Deck(1)
        player1 = Player(200)
        player2 = Player(200)
        players = [player1, player2]
        deck.deal_cards(players)
        self.assertEqual(len(deck), 48)
        self.assertEqual(len(player1.get_hand()), 2)
        self.assertEqual(len(player2.get_hand()), 2)


class TestPolymorphMoveAllCardsMethods(unittest.TestCase):
    def test_move_all_cards(self):
        deck = Deck(1)
        discard_pile = Deck(0)
        player1 = Player(200)
        dealer = Dealer()
        players = [player1, dealer]
        deck.deal_cards(players)
        for player in players:
            player.move_all_cards(discard_pile)
        self.assertEqual(len(deck), 48)
        self.assertEqual(len(discard_pile), 4)
        self.assertEqual(len(player1.get_hand()), 0)
        self.assertEqual(len(dealer.get_hand()), 0)
        for card in discard_pile:
            self.assertIsInstance(card, Card)
