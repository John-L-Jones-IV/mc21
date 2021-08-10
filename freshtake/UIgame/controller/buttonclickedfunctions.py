#!/usr/bin/evn python3
def menu_button_clicked(game):
    print("menu button clicked!")


def hit_button_clicked(game):
    print("hit button clicked!")
    game.hit_player()


def stand_button_clicked(game):
    print("stand button clicked!")
    game.stand_player()


def surrender_button_clicked(game):
    print("surrender button clicked!")


def split_button_clicked(game):
    print("split button clicked!")
    # TODO: code smell! should only comunticate through controller
    game.split_player()


#    deck = game.deck
#    player = game.player1
#    player.split_hand()
#    card = deck.pop()
#    card.set_showing(True)
#    player.get_hand().add_card(card)
#    card = deck.pop()
#    card.set_showing(True)
#    player.get_hand(player.get_active_hand_index() - 1).add_card(card)


def double_button_clicked(game):
    print("double button clicked!")


def deal_button_clicked(game):
    print("deal button clicked!")
