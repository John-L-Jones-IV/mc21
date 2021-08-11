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
    game.split_player()

def double_button_clicked(game):
    print("double button clicked!")
    game.double_player()

def deal_button_clicked(game):
    print("deal button clicked!")
    game.deal_cards()
