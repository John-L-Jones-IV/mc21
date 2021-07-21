#!/usr/bin/env python3
import unittest
from cardcollection import CardCollection
from players import Dealer, Player

class TestPlayerMethods(unittest.TestCase):

    def test_set_get_wager(self):
        p = Player()
        for x in range(1, 10):
            p.set_wager(x)
            self.assertEqual(x, p.get_wager())

    @unittest.expectedFailure
    def test_set_get_wager(self):
        p = Player()
        self.assertRaises(ValueError, p.set_wager(0))
        self.assertRaises(ValueError, p.set_wager(-1))

    def test_get_hand_value(self):
        p = Player()
        p.add_card_to_hand(3)
        self.assertEqual(p.get_hand_value(), 3)
        p.add_card_to_hand(4)
        self.assertEqual(p.get_hand_value(), 7)
        p.add_card_to_hand(2)
        self.assertEqual(p.get_hand_value(), 9)

    def test_get_hand_len(self):
        p = Player()
        p.add_card_to_hand(3)
        self.assertEqual(p.get_hand_len(), 1)
        p.add_card_to_hand(4)
        self.assertEqual(p.get_hand_len(), 2)
        p.add_card_to_hand(4)
        self.assertEqual(p.get_hand_len(), 3)
        
    def test_add_card_to_hand_AND_move_all_card(self):
        p = Player()
        empty_cc = CardCollection()
        dest_cc = CardCollection()
        p.add_card_to_hand(3)
        p.add_card_to_hand(4)
        p.add_card_to_hand(10)
        self.assertEqual(empty_cc, dest_cc)
        p.move_all_cards(dest_cc)
        self.assertEqual(empty_cc, p.hand)
        expected_dest = CardCollection()
        expected_dest[3] = 1
        expected_dest[4] = 1
        expected_dest[10] = 1
        self.assertEqual(dest_cc, expected_dest)


class TestDealerMethods(unittest.TestCase):

    def test_add_card_to_hand_AND_move_all_card(self):
        d = Dealer()
        empty_cc = CardCollection()
        dest_cc = CardCollection()
        d.add_card_to_hand(3)
        d.add_card_to_hand(4)
        d.add_card_to_hand(10)
        self.assertEqual(empty_cc, dest_cc)
        d.move_all_cards(dest_cc)
        self.assertEqual(empty_cc, d.hand)
        expected_dest = CardCollection()
        expected_dest[3] = 1
        expected_dest[4] = 1
        expected_dest[10] = 1
        self.assertEqual(dest_cc, expected_dest)

    def test_get_face_up_card_AND_get_face_down_card(self):
        d = Dealer()
        empty_cc = CardCollection()
        dest_cc = CardCollection()
        d.add_card_to_hand(3)
        self.assertEqual(d.get_face_up_card(), 3)
        d.add_card_to_hand(4)
        self.assertEqual(d.get_face_down_card(), 4)

    def test_get_hand_value(self):
        d = Dealer()
        d.add_card_to_hand(3)
        self.assertEqual(d.get_hand_value(), 3)
        d.add_card_to_hand(4)
        self.assertEqual(d.get_hand_value(), 7)
        d.add_card_to_hand(2)
        self.assertEqual(d.get_hand_value(), 9)

    def test_get_hand_len(self):
        d = Dealer()
        d.add_card_to_hand(3)
        self.assertEqual(d.get_hand_len(), 1)
        d.add_card_to_hand(4)
        self.assertEqual(d.get_hand_len(), 2)
        d.add_card_to_hand(4)
        self.assertEqual(d.get_hand_len(), 3)


if __name__ == '__main__':
    unittest.main()

