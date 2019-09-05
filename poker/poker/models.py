from collections import Counter
from itertools import product, groupby
from random import sample

from django.db import models
from django.utils.functional import cached_property

from .enums import Colour, Face


HAND_VALUES_ORDER = (
    'highcard', 'pair', 'two_pair', 'three_of_kind', 'straight', 'flush', 'full_house',
    'four_of_kind', 'straight_flush', 'royal_flush',
)


class Hand(models.Model):
    player_name = models.TextField()    # In a real-life app it would be a FK to Player model

    class Meta:
        app_label = 'poker'

    @cached_property
    def highcard(self):
        '''
        Simple value of the card. Lowest: 2 - Highest: Ace.
        '''
        return self.score

    @cached_property
    def pair(self):
        '''
        Two cards with the same value.
        '''
        if self._numbers_of_pairs == 1:
            return self.score

    @cached_property
    def two_pair(self):
        '''
        Two times two cards with the same value.
        '''
        if self._numbers_of_pairs == 2:
            return self.score

    @cached_property
    def three_of_kind(self):
        '''
        Three cards with the same value.
        '''
        res = {k: v for k, v in self._group_by_face.items() if len(v) == 3}
        if res:
            return self.score
            
    @cached_property
    def straight(self):
        '''
        Sequence of 5 cards in increasing value (Ace can precede 2 and follow up King).
        '''
        seq = sorted(self._cards, key=lambda o: o.face)
        if not len(seq):
            return
        src_seq = [card.face for card in seq]
        trg_seq = list(range(seq[0].face, seq[0].face + 5))
        if src_seq == trg_seq:
            return self.score

    @cached_property
    def flush(self):
        '''
        5 cards of the same suit.
        '''
        res = {k: v for k, v in self._group_by_colour.items() if len(v) == 5}        
        if res:
            return self.score

    @cached_property
    def full_house(self):
        '''
        Combination of three of a kind and a pair.
        '''
        if self.three_of_kind and self.pair:
            return self.score

    @cached_property
    def four_of_kind(self):
        '''
        Four cards of the same value.
        '''
        res = {k: v for k, v in self._group_by_face.items() if len(v) == 4}
        if res:
            return self.score

    @cached_property
    def straight_flush(self):
        '''
        Straight of the same suit.
        '''
        if self.straight and self.flush:
            return self.score

    @cached_property
    def royal_flush(self):
        '''
        Straight flush from Ten to Ace.
        '''
        if self.straight:
            if sorted(self._cards, key=lambda o: o.face)[0].face == 10:
                return self.score

    @cached_property
    def results(self):
        for item in HAND_VALUES_ORDER[::-1]:
            value = getattr(self, item)
            if value:
                return item, value

    def _group_by(self, keyfunc):
        cards = {}
        data = sorted(self._cards, key=keyfunc)
        for k, g in groupby(data, key=keyfunc):
            cards[k] = list(g)
        return cards

    @cached_property
    def _group_by_face(self):
        return self._group_by(keyfunc=lambda o: o.face)

    @cached_property
    def _group_by_colour(self):
        return self._group_by(keyfunc=lambda o: o.colour)

    @cached_property
    def _pairs(self):
        return {k: v for k, v in self._group_by_face.items() if len(v) == 2}

    @cached_property
    def _numbers_of_pairs(self):
        return len(self._pairs)

    @cached_property
    def _cards(self):
        return self.cards.all()

    def __repr__(self):
        # In real app it is a bad idea to use related entities due to extra queries
        cards = ', '.join([str(card) for card in self.cards])
        return f'{self.__class__.__name__} <{self.player_name}\'s cards: {cards}>'


class Card(models.Model):
    hand = models.ForeignKey(
        'poker.Hand',
        on_delete=models.CASCADE,
        related_name='cards',
    )
    face = models.IntegerField(
        choices=[(name, name) for name in Face]
    )
    colour = models.IntegerField(
        choices=[(name, name) for name in Colour]
    )

    class Meta:
        app_label = 'poker'
        unique_together = (
            ('hand', 'face', 'colour',),
        )

    @cached_property
    def colour_repr(self):
        return Colour(self.colour).name

    @cached_property
    def face_repr(self):
        return Face(self.face).name
    
    def __repr__(self):
        return f'{self.__class__.__name__}<{self.face_repr} {self.colour_repr}>'
