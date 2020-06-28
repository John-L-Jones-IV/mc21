from blackjack import Player, Dealer


class SimplePlayer(Player):
    def __init__(self, balence, deck, used_cards, cards_showing):
        Player.__init__(self, balence, deck, used_cards, cards_showing)

    def move(self):
        if self.best_hand_val() >= 17:
            self.stand()
        elif self.best_hand_val() == 0:
            self.stand()
        else:
            self.hit()


class BasicStratPlayer(Player):
    def __init__(self, balence, deck, used_cards, cards_showing, dealer):
        """
        Used strategy from wizzard of odds.
        Don't. It sucks.
        https://wizardofodds.com/games/blackjack/strategy/4-decks/
        """
        Player.__init__(self, balence, deck, used_cards, cards_showing)
        self.dealer = dealer

    def move(self):
        dealer_showing = self.dealer.hand[0].get_num_val()
        if self.best_hand_val() == 0:
            self.stand()
        # SPLITS
        elif ((len(self.hand) == 2 and self.hand[0].val == self.hand[1].val and
                len(self.split_hand) == 0) and self.status == Status.PLAY and
                not (self.hand[0].val == 'J' or
                self.hand[0].val == '5' or self.hand[0].val == 'K' or
                self.hand[0].val == 'Q' or self.hand[0].val == '10')):
            card_val = self.hand[0].val
            if card_val == 'A':
                self.split()
            elif card_val == '8':
                self.split()
            elif card_val == '9':
                if (dealer_showing == 7 or
                        10 <= dealer_showing <= 11):
                    self.stand()
                else:
                    self.split()
            elif card_val == '7':
                if dealer_showing <= 7:
                    self.split()
                else:
                    self.hit()
            elif card_val == '6':
                if dealer_showing <= 6:
                    self.split()
                else:
                    self.hit()
            elif card_val == '4':
                if 5 <= dealer_showing <= 6:
                    self.split()
                else:
                    self.hit()
            elif card_val == '2' or card_val == '3':
                if dealer_showing <= 7:
                    self.split()
                else:
                    self.hit()
        # SOFT
        elif (14 <= self.hand_val(hard=False) <= 21 and
                self.hand_val(hard=False) !=  self.hand_val(hard=True)):
            soft_val = self.hand_val(hard=False)
            if soft_val >= 19:
                self.stand()
            elif 9 <= dealer_showing <= 11:
                self.hit()
            elif soft_val == 18:
                if 3 <= dealer_showing <= 6:
                    self.double()
                else:
                    self.stand()
            elif 7 <= dealer_showing:
                self.hit()
            elif soft_val == 17:
                if dealer_showing == 2:
                    self.hit()
                else:
                    self.double()
            elif 15 <= soft_val <= 16:
                if 2 <= dealer_showing <= 3:
                    self.hit()
                else:
                    self.double()
            elif soft_val == 14:
                if 2 <= dealer_showing <= 4:
                    self.hit()
                else:
                    self.double()
        # HARD
        else:
            hand_val = self.hand_val()
            if hand_val >= 17:
                self.stand()
            elif 13 <= hand_val <= 16:
                if dealer_showing <= 6:
                    self.stand()
                else:
                    self.hit()
            elif hand_val == 12:
                if 4 <= dealer_showing <= 6:
                    self.stand()
                else:
                    self.hit()
            elif hand_val == 11:
                if dealer_showing == 11:
                    self.hit()
                else:
                    self.double()
            elif hand_val == 10:
                if dealer_showing >= 10:
                    self.hit()
                else:
                    self.double()
            elif hand_val == 9:
                if 3 <= dealer_showing <= 6:
                    self.double()
                else:
                    self.hit()
            else:
                self.hit()


class BasicStrategyPlayer2(Player):
    """
    Use baseic strategy from Beat the Dealer by Edward Thorp.
    """
    def __init__(self, balence, deck, used_cards, cards_showing, dealer):
        Player.__init__(self, balence, deck, used_cards, cards_showing)
        self.dealer = dealer

    def move(self):
        dealer_showing = self.dealer.hand[0].get_num_val()
        if self.best_hand_val() == 0 or self.best_hand_val() == 21:
            self.stand()
        # Splits
        elif (self.status == Status.PLAY and
              len(self.hand) == 2 and len(self.split_hand) == 0 and
              self.hand[0].get_num_val() == self.hand[1].get_num_val()):
            pair = self.hand[0].get_num_val()
            if pair == 11:
                self.split()
            elif pair == 10:
                pass
            elif pair == 9:
                if (dealer_showing != 7 or dealer_showing != 10
                    or dealer_showing != 11):
                    self.split()
            elif pair == 8:
                self.split()
            elif pair == 7:
                if dealer_showing <= 8:
                    self.split()
            elif pair == 6:
                if dealer_showing <= 7:
                    self.split()
            elif pair == 5:
                pass
            elif pair == 4:
                if dealer_showing == 5:
                    self.split()
            elif pair == 3 or pair == 2:
                if dealer_showing <= 7:
                    self.split()
        # Doubles
        # TODO

        # Play
        hard_hand = self.hand_val()
        soft_hand = self.hand_val(hard=False)
        if dealer_showing == 2:
            if hard_hand < 13 and soft_hand < 18:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 3:
            if hard_hand < 13 and soft_hand < 18:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 4:
            if hard_hand < 12 and soft_hand < 18:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 5:
            if hard_hand < 12 and soft_hand < 18:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 6:
            if hard_hand < 12 and soft_hand < 18:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 7:
            if hard_hand < 17 and soft_hand < 18:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 8:
            if hard_hand < 17 and soft_hand < 18:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 9:
            if hard_hand < 17 and soft_hand < 18:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 10:
            if hard_hand < 17 and soft_hand < 19:
                self.hit()
            else:
                self.stand()
        if dealer_showing == 11:
            if hard_hand < 17 and soft_hand < 18:
                self.hit()
            else:
                self.stand()

class BasicStrategyPlayer3(Player):
    """
    Use strategy from:
    https://github.com/lukysummer/Monte-Carlo-Control-for-Blackjack.
    """
    def __init__(self, balence, deck, used_cards, cards_showing, dealer):
        Player.__init__(self, balence, deck, used_cards, cards_showing)
        self.dealer = dealer

    def usable_ace(self):
        return (self.hand_val() != self.hand_val(hard=True) and
                self.hand_val() <= 21)

    def move(self):
        dealer_showing = self.dealer.hand[0].get_num_val()

        if self.best_hand_val() == 0 or self.best_hand_val() == 21:
            self.stand()

        elif self.usable_ace():
            if  2 <= dealer_showing <= 8:
                if self.best_hand_val() <= 17:
                    self.hit()
                else:
                    self.stand()
            else:
                if self.best_hand_val() <= 18:
                    self.hit()
                else:
                    self.stand()
        else:
            if 7 <= dealer_showing <= 11:
                if self.best_hand_val() <= 16:
                    self.hit()
                else:
                    self.stand()
            elif 2 <= dealer_showing <= 3:
                if self.best_hand_val() <= 12:
                    self.hit()
                else:
                    self.stand()
            elif 4 <= dealer_showing <= 6:
                if self.best_hand_val() <= 11:
                    self.hit()
                else:
                    self.stand()


class CCPlayer(Player):
    """
    Card Counting Player.
    """
    def __init__(self, balence, deck, used_cards, cards_showing, dealer):
        Player.__init__(balence, deck, used_cards, cards_showing)
        self.dealer = dealer

    def move(self):
        pass # TODO

    def set_wager(self, wager):
        pass # TODO


class HLPlayer(BasicStratPlayer):
    """
    Player using high low counting system.
    """
    def __init__(self, balence, deck, used_cards, cards_showing, dealer):
        BasicStratPlayer.__init__(
                self,
                balence,
                deck,
                used_cards,
                cards_showing,
                dealer
            )

    def set_wager(self, wager):
        running_cnt = 0
        for card in self.deck:
            if card.val == 'Blank':
                continue
            val = card.get_num_val()
            if 2 <= val <= 6:
                running_cnt += 1
            elif 10 <= val <= 11:
                running_cnt -= 1
        L = len(self.deck)
        decks_remaining = L//26
        decks_remaining = 1 if decks_remaining < 1 else decks_remaining
        tru_cnt = running_cnt/float(decks_remaining)
        bet = wager*(tru_cnt)
        if bet < 1:
            bet = wager
        if bet > 50:
            bet = 50
        self.wager = bet
