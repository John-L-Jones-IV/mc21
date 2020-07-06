#!/usr/bin/env python3
"""
test_strategy.py
Unittest for strategy.py

John L. Jones IV
"""
import unittest
from strategy import Node, add_link, value_of_chain, prob_of_chain
from strategy import DealerProbabilityTree, get_dealer_pmf


class Test_Node(unittest.TestCase):
    def test_get_int_value(self):
        node = Node('A')
        self.assertEqual(node.get_int_value(), 11)
        self.assertEqual(node.get_int_value(False), 1)
        node = Node('2')
        self.assertEqual(node.get_int_value(), 2)
        node = Node('3')
        self.assertEqual(node.get_int_value(), 3)
        node = Node('4')
        self.assertEqual(node.get_int_value(), 4)
        node = Node('5')
        self.assertEqual(node.get_int_value(), 5)
        node = Node('6')
        self.assertEqual(node.get_int_value(), 6)
        node = Node('7')
        self.assertEqual(node.get_int_value(), 7)
        node = Node('8')
        self.assertEqual(node.get_int_value(), 8)
        node = Node('9')
        self.assertEqual(node.get_int_value(), 9)
        node = Node('10')
        self.assertEqual(node.get_int_value(), 10)
        node = Node('K')
        self.assertEqual(node.get_int_value(), 10)
        node = Node('Q')
        self.assertEqual(node.get_int_value(), 10)
        node = Node('J')
        self.assertEqual(node.get_int_value(), 10)
        with self.assertRaises(ValueError):
            node = Node('1')


class Test_Functions(unittest.TestCase):
    def test_add_link(self):
        n2 = Node('2')
        n3 = Node('3')
        n4 = Node('4')
        add_link(n4, n2, 0.96)
        self.assertEqual(n4.fwd_links[0][0], n2)
        self.assertEqual(n4.fwd_links[0][1], 0.96)
        self.assertEqual(n4.bwd_link, None)
        self.assertEqual(n2.fwd_links, [])
        self.assertEqual(n2.bwd_link[0], n4)
        self.assertEqual(n2.bwd_link[1], 0.96)
        self.assertEqual(n3.fwd_links, [])
        self.assertEqual(n3.bwd_link, None)

    def test_value_of_chain(self):
        n1 = Node('5')
        n2 = Node('5')
        n3 = Node('5')
        add_link(n1, n2, 0.5)
        add_link(n2, n3, 0.5)
        self.assertEqual(value_of_chain(n3), 15)

        n4 = Node('A')
        n5 = Node('5')
        n6 = Node('5')
        add_link(n4, n5, 0.5)
        add_link(n5, n6, 0.5)
        self.assertEqual(value_of_chain(n6), 21)

        n7 = Node('A')
        n8 = Node('5')
        n9 = Node('6')
        add_link(n7, n8, 0.5)
        add_link(n8, n9, 0.5)
        self.assertEqual(value_of_chain(n9), 12)

        with self.assertRaises(AssertionError):
            value_of_chain(n8)

    def test_prob_of_chain(self):
        n1 = Node('5')
        n2 = Node('5')
        n3 = Node('5')
        add_link(n1, n2, 0.5)
        add_link(n2, n3, 0.5)
        self.assertEqual(prob_of_chain(n3), 0.25)

        n4 = Node('A')
        n5 = Node('5')
        n6 = Node('6')
        add_link(n4, n5, 1.0/52.0)
        add_link(n5, n6, 1.0/51.0)
        self.assertEqual(prob_of_chain(n6), 1.0/52.0*1.0/51.0)

        with self.assertRaises(AssertionError):
            value_of_chain(n5)

    def test_get_dealer_pmf(self):
        deck_pmf = {'A': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0,
                    '5': 10,
                    '6': 10,
                    '7': 0,
                    '8': 0,
                    '9': 0,
                    '10': 0}
        bot = float(20*19*18)
        expected_pmf = {0: 0.0,
                        17: 8*9*10/bot,
                        18: 3*9*10*10/bot,
                        19: 3*9*10*10/bot,
                        20: 8*9*10/bot,
                        21: 0.0}
        self.assertEqual(get_dealer_pmf('2', deck_pmf), expected_pmf)


class Test_DealerProbabilityTree(unittest.TestCase):
    def test_get_end_nodes(self):
        pmf1 = {'2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                '7': 0,
                '8': 0,
                '9': 0,
                '10': 10,
                'A': 0}
        tree1 = DealerProbabilityTree('A', pmf1)
        pmf2 = {'A': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 10,
                '6': 10,
                '7': 0,
                '8': 0,
                '9': 0,
                '10': 0}
        tree2 = DealerProbabilityTree('2', pmf2)

        for node in tree1.get_end_nodes():
            self.assertEqual(node.value, '10')
        self.assertEqual(len(tree1.get_end_nodes()), 1)
        self.assertEqual(len(tree2.get_end_nodes()), 8)

    def test_get_end_nodes(self):
        pmf1 = {'A': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 0,
                '6': 0,
                '7': 0,
                '8': 0,
                '9': 0,
                '10': 10}
        tree1 = DealerProbabilityTree('A', pmf1)
        expected_pmf = {0: 0.0,
                        17: 0.0,
                        18: 0.0,
                        19: 0.0,
                        20: 0.0,
                        21: 1.0}
        self.assertEqual(tree1.get_dealer_score_pmf(), expected_pmf)

        pmf2 = {'A': 0,
                '2': 0,
                '3': 0,
                '4': 0,
                '5': 10,
                '6': 10,
                '7': 0,
                '8': 0,
                '9': 0,
                '10': 0}
        tree2 = DealerProbabilityTree('2', pmf2)
        bot = float(20*19*18)
        expected_pmf = {0: 0.0,
                        17: 8*9*10/bot,
                        18: 3*9*10*10/bot,
                        19: 3*9*10*10/bot,
                        20: 8*9*10/bot,
                        21: 0.0}
        self.assertEqual(tree2.get_dealer_score_pmf(), expected_pmf)


if __name__ == '__main__':
    unittest.main()
