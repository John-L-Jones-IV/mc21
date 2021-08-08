#!/usr/bin/evn python3
def menu_button_clicked(game_vars):
    print("menu button clicked!")


def hit_button_clicked(game_vars):
    print("hit button clicked!")
    
    game_vars.deck.hit(game_vars.player1)


def stand_button_clicked(game_vars):
    print("stand button clicked!")
    # TODO: code smell! should only comunticate through controller
    if game_vars.player1.active_hand > 0:
        game_vars.player1.active_hand -= 1
    else:
        game_vars.state = game_vars.GameState.EVALUATE_RESULTS


def surrender_button_clicked(game_vars):
    print("surrender button clicked!")


def split_button_clicked(game_vars):
    print("split button clicked!")
    # TODO: code smell! should only comunticate through controller
    deck = game_vars.deck
    player = game_vars.player1
    player.split_hand()
    card = deck.pop()
    card.set_showing(True)
    player.get_hand().append(card)
    card = deck.pop()
    card.set_showing(True)
    player.get_hand(player.get_active_hand() - 1).append(card)


def double_button_clicked(game_vars):
    print("double button clicked!")


def deal_button_clicked(game_vars):
    print("deal button clicked!")
