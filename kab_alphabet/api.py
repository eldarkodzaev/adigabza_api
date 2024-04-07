from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework.response import Response

from adigabza_api.settings.base import CACHE_24_HOURS

from .models import KabLetter
from .serializers import KabLetterSerializer, KabLetterWithWordsSerializer


class KabAlphabetViewset(viewsets.ReadOnlyModelViewSet):
    queryset = KabLetter.objects.all()
    serializer_class = KabLetterSerializer
    lookup_field = 'slug'

    @method_decorator(cache_page(CACHE_24_HOURS))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        letter_instance = self.get_object()
        serializer = KabLetterWithWordsSerializer(letter_instance)
        return Response(serializer.data)
