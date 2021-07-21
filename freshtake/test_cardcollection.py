#!/usr/bin/env python3
import unittest
from cardcollection import CardCollection

class TestCardCollectionMethods(unittest.TestCase):

    def setUp(self):
        self.cc = CardCollection()

    def test_init(self):
        for k in self.cc:
            self.assertEqual(self.cc.get(k), 0)

    def test_set_get(self):
        self.cc[2] = 1
        self.cc[11] = 2
        self.assertEqual(self.cc.get(2), 1)
        self.assertEqual(self.cc.get(11), 2)
        self.assertEqual(self.cc.get(3), 0)
        self.assertEqual(self.cc.get(4), 0)
        self.assertEqual(self.cc.get(8), 0)

    @unittest.expectedFailure
    def test_bad_get(self):
        self.assertRaises(TypeError, self.cc.get("2"))
        self.assertRaises(TypeError, self.cc.get(True))
        self.assertRaises(ValueError, self.cc.get(1))
        self.assertRaises(ValueError, self.cc.get(12))

    @unittest.expectedFailure
    def test_bad_set(self):
        with self.assertRaises(TypeError):
            self.cc["2"] = 1
        with self.assertRaises(ValueError):
            self.cc[1] = 2
        with self.assertRaises(ValueError):
            self.cc[12] = 2

    def test_repr_(self):
        a = '{2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}'
        self.assertEqual(str(self.cc), a)


    def test_iter_(self):
        self.cc[5] = 2
        for k in self.cc:
            if k == 5:
                self.assertEqual(self.cc.get(k), 2)
            else:
                self.assertEqual(self.cc.get(k), 0)

    def test_get_num_cards(self):
        self.assertEqual(self.cc.get_num_cards(), 0)
        self.cc[2] = 1;
        self.assertEqual(self.cc.get_num_cards(), 1)
        self.cc[3] = 1;
        self.assertEqual(self.cc.get_num_cards(), 2)
        self.cc[8] = 2;
        self.assertEqual(self.cc.get_num_cards(), 4)

    def test__len__(self):
        self.assertEqual(len(self.cc), 0)
        self.cc[2] = 1;
        self.assertEqual(len(self.cc), 1)
        self.cc[3] = 1;
        self.assertEqual(len(self.cc), 2)
        self.cc[8] = 2;
        self.assertEqual(len(self.cc), 4)

    def test_move_all_cards(self):
        cc1 = CardCollection()
        cc2 = CardCollection()
        cc1[2] = 2
        cc1[5] = 1
        cc1[10] = 1
        cc1.move_all_cards(cc2)
        self.assertEqual(cc2[2], 2)
        self.assertEqual(cc2[5], 1)
        self.assertEqual(cc2[10], 1)
        self.assertEqual(cc1[2], 0)
        self.assertEqual(cc1[5], 0)
        self.assertEqual(cc1[10], 0)
        self.assertEqual(cc1[4], 0)
        self.assertEqual(cc2[6], 0)
        self.assertEqual(cc2[11], 0)

    def test_get_aceis11_total(self):
        self.cc[10] = 1
        self.assertEqual(self.cc._get_aceis11_total(), 10)
        self.cc[2] = 3
        self.assertEqual(self.cc._get_aceis11_total(), 16)
        self.cc[11] = 1
        self.assertEqual(self.cc._get_aceis11_total(), 27)

    def test_get_aceis1_toal(self):
        self.cc[10] = 1
        self.assertEqual(self.cc._get_aceis1_total(), 10)
        self.cc[2] = 3
        self.assertEqual(self.cc._get_aceis1_total(), 16)
        self.cc[11] = 1
        self.assertEqual(self.cc._get_aceis1_total(), 17)

    def test_get_total_value(self):
        self.cc[11] = 1
        self.assertEqual(self.cc.get_total_value(), 11)
        self.cc[3] = 1
        self.assertEqual(self.cc.get_total_value(), 14)
        self.cc[2] = 1
        self.assertEqual(self.cc.get_total_value(), 16)
        self.cc[10] = 1
        self.assertEqual(self.cc.get_total_value(), 16)
        self.cc[2] = 2
        self.assertEqual(self.cc.get_total_value(), 18)
        self.cc[5] = 1
        self.assertEqual(self.cc.get_total_value(), 23)


if __name__ == '__main__':
    unittest.main()

