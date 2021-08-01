#!/usr/bin/env python3
import os
from PIL import Image

# All dimensions are in pixels
X_PATTERN_SPACING, Y_PATTERN_SPACING = 390, 570
CROP_WIDTH, CROP_HEIGHT = 360, 540
X_START, Y_START = 30, 30

ROW_NAMES = ["spades", "hearts", "diamonds", "clubs"]
COL_NAMES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

SOURCE_IMG_PATH = "English_pattern_playing_cards_deck.png"
OUTPUT_DIR = "cards"

if __name__ == "__main__":

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    with Image.open(SOURCE_IMG_PATH) as src_img:
        for row_cnt, row_val in enumerate(ROW_NAMES):
            for col_cnt, col_val in enumerate(COL_NAMES):
                box = (
                    X_START + col_cnt * X_PATTERN_SPACING,
                    Y_START + row_cnt * Y_PATTERN_SPACING,
                    CROP_WIDTH + X_START + col_cnt * X_PATTERN_SPACING,
                    CROP_HEIGHT + Y_START + row_cnt * Y_PATTERN_SPACING,
                )
                crop_img = src_img.crop(box)
                crop_img_name = os.path.join(
                    OUTPUT_DIR, row_val + "_" + col_val + ".png"
                )
                crop_img.save(crop_img_name)

    src_img.load()  # .load() closes the file in case of failure.