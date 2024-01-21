from rest_framework import viewsets
from rest_framework.response import Response

from kab_alphabet.models import KabLetter
from .serializers import KabLetterSerializer, KabLetterWithWordsSerializer


class KabAlphabetViewset(viewsets.ReadOnlyModelViewSet):
    queryset = KabLetter.objects.all()
    serializer_class = KabLetterSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        letter_instance = self.get_object()
        serializer = KabLetterWithWordsSerializer(letter_instance)
        return Response(serializer.data)
