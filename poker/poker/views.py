from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Hand
from .serializers import HandSerializer, CardSerializer


class HandListCreateApiView(generics.ListCreateAPIView):
    queryset = Hand.objects.prefetch_related('cards')
    serializer_class = HandSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            cards = request.data.get('cards', [])
            if len(cards) != 5:
                return Response({
                    'errors': ['Hand should include exactly 5 cards.']
                }, status=status.HTTP_400_BAD_REQUEST)
            for raw_card in cards:
                raw_card['hand'] = obj.id
                card_serializer = CardSerializer(data=raw_card)
                if not card_serializer.is_valid():
                    return Response(card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                card_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)