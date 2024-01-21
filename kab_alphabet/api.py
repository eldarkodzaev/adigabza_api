from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings

from rest_framework import viewsets
from rest_framework.response import Response

from kab_alphabet.models import KabLetter
from .serializers import KabLetterSerializer, KabLetterWithWordsSerializer


class KabAlphabetViewset(viewsets.ReadOnlyModelViewSet):
    queryset = KabLetter.objects.all()
    serializer_class = KabLetterSerializer
    lookup_field = 'slug'

    @method_decorator(cache_page(settings.CACHE_24_HOURS))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        letter_instance = self.get_object()
        serializer = KabLetterWithWordsSerializer(letter_instance)
        return Response(serializer.data)
