from rest_framework import serializers

from .models import Hand, Card


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'id', 'hand', 'face', 'colour', 'face_repr', 'colour_repr',
        )


class HandSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    results = serializers.ReadOnlyField()

    class Meta:
        model = Hand
        fields = ('id', 'player_name', 'cards', 'results',)