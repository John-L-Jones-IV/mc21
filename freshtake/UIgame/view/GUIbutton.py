#!/usr/bin/evn python3
from __future__ import annotations
from typing import Tuple

import pygame

# Colors
BLACK = (0x00, 0x00, 0x00)

# Fonts
pygame.font.init()
FONT_SIZE = 30
FONT = pygame.font.SysFont("comicsans", FONT_SIZE)


class UIButton:
    # static attributes, same for all instances of UIButton.
    BORDER_RADIUS = 5
    ACTIVE_TEXT_COLOR = BLACK
    NON_ACTIVE_TEXT_COLOR = BLACK
    ACTIVE_BTN_COLOR = (0xAA, 0xAA, 0xAA)
    NON_ACTIVE_BTN_COLOR = (0x55, 0x55, 0x55)

    def __init__(self, dimensions, text, function):
        self.active = True
        self.hidden = False
        x_position, y_position, width, height = dimensions
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.text = text
        self.function = function

    def set_active(self, activeState: bool) -> None:
        self.active = activeState

    def set_hidden(self, hiddenState: bool) -> None:
        self.hidden = hiddenState

    def get_dimensions(self):
        return (self.x_position, self.y_position, self.width, self.height)

    def is_mouse_position_colliding(self, mouse_pos: Tuple[int, int]) -> bool:
        if self.hidden or not self.active:
            return False
        mouse_x, mouse_y = mouse_pos
        if not (self.x_position <= mouse_x <= self.x_position + self.width):
            return False
        if not (self.y_position <= mouse_y <= self.y_position + self.height):
            return False
        return True

    def draw(self, surface):
        if self.hidden:
            return
        x, y, w, h = self.get_dimensions()
        rect = pygame.Rect(x, y, w, h)
        self._draw_button(surface, rect)
        self._draw_text(surface, rect)

    @staticmethod
    def _find_pos_of_smaller_rect_centered(
        large_rect: pygame.Rect(), small_rect: pygame.Rect()
    ) -> Tuple[int, int]:
        """
        Given a large and small rectangle return the position needed
        to place the small rectange directly in the center of the large
        rectangle.

        Use to center the text image on the button image for UIButton.
        """
        large_width, large_height = large_rect.size
        small_width, small_height = small_rect.size
        x_offset = (large_width - small_width) / 2
        y_offset = (large_height - small_height) / 2
        small_x = int(large_rect.x + x_offset)
        small_y = int(large_rect.y + y_offset)
        return small_x, small_y

    def _draw_button(self, surface, rect):
        if self.active:
            color = self.ACTIVE_BTN_COLOR
        else:
            color = self.NON_ACTIVE_BTN_COLOR
        pygame.draw.rect(surface, color, rect, border_radius=UIButton.BORDER_RADIUS)

    def _draw_text(self, surface, rect):
        if self.active:
            text_color = self.ACTIVE_TEXT_COLOR
        else:
            text_color = self.NON_ACTIVE_TEXT_COLOR
        font = pygame.font.SysFont(None, FONT_SIZE)
        text_img = font.render(self.text, True, text_color)
        text_rect = text_img.get_rect()
        text_x, text_y = UIButton._find_pos_of_smaller_rect_centered(rect, text_rect)
        surface.blit(text_img, (text_x, text_y))
