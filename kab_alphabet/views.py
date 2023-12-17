from rest_framework import generics

from kab_alphabet.models import KabLetter
from .serializers import KabLetterSerializer


class KabAlphabetAPIListView(generics.ListAPIView):
    serializer_class = KabLetterSerializer
    queryset = KabLetter.objects.all()


class KabLetterAPIDetailView(generics.RetrieveAPIView):
    serializer_class = KabLetterSerializer
    queryset = KabLetter.objects.all()
    lookup_field = 'slug'
