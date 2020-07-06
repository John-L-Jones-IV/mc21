#!/usr/bin/env python3
"""
strategy.py
Classes and functions for statistical blackjack strategy

John L. Jones IV
"""


class DealerProbabilityTree(object):
    """
    Used to generate probabiltiy tree given the hit until 17 strategy.
    """
    def __init__(self, dealer_showing_value, deck_pmf):
        """
        Build a DealerProbabilityTree.

        dealer_showing_value    - value of card the dealer has face up as
        string in ['2', '3', '4', '5', '6', '7', '8', '9' '10', 'A']
        pmf_deck    - a dictionary of card value/number remaining in deck
        (key/value) pairs
        """
        self.base_node = Node(dealer_showing_value)
        self.end_nodes = []
        deck_pmf_cpy = deck_pmf.copy()
        self._grow_tree(self.base_node, deck_pmf_cpy)

    def get_dealer_score_pmf(self):
        """
        Return the dealer's pmf of score given the hit until 17 strategy is
        used.
        """
        score_pmf = {0: 0.0,
                     17: 0.0,
                     18: 0.0,
                     19: 0.0,
                     20: 0.0,
                     21: 0.0}
        for node in self.get_end_nodes():
            value = value_of_chain(node)
            if 0 < value < 17:
                raise ValueError
            prob = prob_of_chain(node)
            score_pmf[value] += prob
        return score_pmf

    def get_end_nodes(self):
        """Return all end nodes in DealerProbabilityTree."""
        return self.end_nodes

    def get_base_node(self):
        return self.base_node

    def _grow_tree(self, node, deck_pmf):
        """
        WARNING: This should should only be used in  __init__().
        _grow_tree() should NOT be be called outside __init__().
        Additional calls will modify self.end_nodes in undesirable ways.

        Grow tree from base_node given deck_pmf.

        base_node   - a _Node class that will be the base of the tree
        deck_pmf    - a dictionary of card value / number of card pairs
        """
        if not 0 < value_of_chain(node) < 17:
            self.end_nodes.append(node)
            return

        deck_pmf_cpy = deck_pmf.copy()

        # TODO: if low on cards average pmf with a fresh shuffle pmf
        if sum(deck_pmf_cpy.values()) == 0:
            return

        for card in deck_pmf_cpy:
            if deck_pmf_cpy[card] <= 0:  # if the card is not in the deck
                continue  # do not create a link & try another card
            P = float(deck_pmf_cpy[card])/float(sum(deck_pmf_cpy.values()))
            new_node = Node(card)
            add_link(node, new_node, P)
            pmf_in = deck_pmf_cpy.copy()
            pmf_in[card] -= 1
            self._grow_tree(new_node, pmf_in)


class Node(object):
    """Nodes contain card values and links through the tree"""
    def __init__(self, value, bwd_link=None, fwd_links=None):
        """
        value   - card value as string (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, A)
        base    - backward Link tuples (Node, probability)
        heads   - list of forward Links tuples (Node, probability)
        """
        assert (bwd_link is None or (type(bwd_link[0]) is Node and
                type(bwd_link[1] is float)))
        if fwd_links is None:
            fwd_links = []  # new empty list
        for link in fwd_links:
            assert type(link[1]) is float, 'link[1] must be a float'
            assert 0.0 <= link[1] <= 1, 'link[1] must be between 0.0 and 1.0'
        if value == 'K' or value == 'Q' or value == 'J':
            value = '10'
        valid_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'A']
        if value not in valid_values:
            raise ValueError('Node must be valid card value. Not  ' +
                             str(value))
        self.value = value
        self.bwd_link = bwd_link
        self.fwd_links = fwd_links

    def __str__(self):
        if self.bwd_link is None:
            str_out = 'None -> ' + self.value + '\n'
        else:
            str_out = self.bwd_link[0].value + ' -> ' + self.value
        for l in self.fwd_links:
            str_out += '\t -> ' + l[0].value + ' P = ' + str(l[1]) + '\n'
        return str_out

    def get_int_value(self, hard=True):
        if self.value == 'A' and hard:
            return 11
        elif self.value == 'A' and not hard:
            return 1
        else:
            return int(self.value)


def add_link(a, b, probability):
    """link _Node a to _Node b (a->b) with probability"""
    assert 0.0 <= probability <= 1.0, 'probability = ' + str(probability)
    if 0.0 < probability <= 1.0:
        b.bwd_link = (a, probability)
        a.fwd_links.append((b, probability))


def value_of_chain(node):
    """step backwards through the links and sum up value of nodes"""
    assert len(node.fwd_links) == 0, 'node must be an end node'
    soft_total = 0
    hard_total = 0
    start_node = node
    while True:
        hard_total += node.get_int_value()
        if node.bwd_link is None:
            break
        node = node.bwd_link[0]
    node = start_node
    while True:
        soft_total += node.get_int_value(False)
        if node.bwd_link is None:
            break
        node = node.bwd_link[0]
    if soft_total > 21:
        return 0
    elif hard_total <= 21:
        return hard_total
    else:
        return soft_total


def prob_of_chain(node):
    assert len(node.fwd_links) == 0, 'node must be an end node'
    assert type(node.bwd_link[0]) is Node, 'link[0] must be type Node'
    assert type(node.bwd_link[1]) is float, 'link[1] must be type float'
    total = 1.00
    while node.bwd_link is not None:
        total *= node.bwd_link[1]
        node = node.bwd_link[0]
    return total


def get_dealer_pmf(dealer_card_showing, deck_pmf):
    tree = DealerProbabilityTree(dealer_card_showing, deck_pmf)
    return tree.get_dealer_score_pmf()
