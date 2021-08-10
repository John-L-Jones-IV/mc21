#!/usr/bin/env python3
import os
from PIL import Image

# All dimensions are in pixels
X_START, Y_START = 7, 7
X_PATTERN_SPACING, Y_PATTERN_SPACING = 98, 143
CROP_WIDTH, CROP_HEIGHT = 91, 137

ROW_NAMES = ["spades", "hearts", "diamonds", "clubs"]
COL_NAMES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

SOURCE_IMG_PATH = "English_pattern_playing_cards_deck_1280x580_no_background.png"
OUTPUT_DIR = "smallcards"


def main():
    ensure_directory(OUTPUT_DIR)
    crop_and_save_macro()


if __name__ == "__main__":
    main()


def ensure_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def crop_and_save_macro():
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
