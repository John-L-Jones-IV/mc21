#!/usr/bin/env python3
import pygame
import os

WINDOW_W, WINDOW_H = 1200, 800
CARD_W = 150
CARD_H = int(35.0/25.0*CARD_W)
print(f"w : {CARD_W}\nh : {CARD_H}")

# Colors
WHITE = (0xFF, 0xFF,0xFF)
BLACK = (0, 0, 0)
# 0x55AA55 green is the background of card sprite source image.
GREEN = (0x55, 0xAA, 0x55)


FPS = 120
CARD_VEL = 10

ICON_IMG = pygame.image.load(os.path.join("assets", "blackjackicon.png"))
pygame.init()
pygame.display.set_caption("mc21 - Blackjack for Humans")
pygame.display.set_icon(ICON_IMG)
window = pygame.display.set_mode((WINDOW_W, WINDOW_H))

test_card_img = pygame.image.load(os.path.join("assets", "cards", "cardback.png"))
test_card = pygame.transform.scale(test_card_img, (CARD_W, CARD_H))
test_card2_img = pygame.image.load(os.path.join("assets", "cards", "spades_A.png"))
test_card2= pygame.transform.scale(test_card2_img, (CARD_W, CARD_H))
card_img_dir = os.path.join("assest", "cards")

def draw_screen():
    window.fill(GREEN)
    #TODO: draw cards and User input buttons
    window.blit(test_card, (200, 200))
    window.blit(test_card2, (400, 200))
    pygame.display.flip()


def main():

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_screen()

    pygame.quit()


if __name__ == '__main__':
    main()
