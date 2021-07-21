#!/usr/bin/env python3
from enum import IntEnum, auto

class Call(IntEnum):
    STAND = auto()
    HIT = auto()
    DOUBLE = auto()
    SPLIT = auto()
    SURRENDER = auto()

class SplitsAllowed(IntEnum):
    ANY_FIRST_TWO_CARDS = auto()
    TWO_HANDS = auto()
    THREE_HANDS = auto()

