from enum import Enum


class Colour(Enum):
    '''
    Representation of card colours, each colour represented by a digit.
    '''
    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4


class Face(Enum):
    '''
    Representation of card faces, each face represented by a digit.
    Higher value represented by bigger digit.
    '''
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
