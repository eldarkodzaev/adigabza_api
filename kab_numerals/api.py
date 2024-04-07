from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from adigabza_api.settings.base import CACHE_24_HOURS

from rest_framework import generics

from .models import KabNaturalNumber
from .pagination import KabNumeralsPagination
from .serializers import KabNaturalNumberSerializer


class KabNumeralsAPIListView(generics.ListAPIView):
    serializer_class = KabNaturalNumberSerializer
    pagination_class = KabNumeralsPagination

    @method_decorator(cache_page(CACHE_24_HOURS))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)    

    def get_queryset(self):
        params = self._get_params()
        return KabNaturalNumber.objects.only(
            'number', 'translate_decimal')[params['start']:params['end'] + 1:params['step']]

    def paginate_queryset(self, queryset):
        if self.request.GET.get('page'):
            return super().paginate_queryset(queryset)

    def _get_params(self):
        try:
            start = abs(int(self.request.GET.get('start')))
        except (ValueError, TypeError):
            start = 1

        try:
            end = abs(int(self.request.GET.get('end')))
        except (ValueError, TypeError):
            end = 100

        try:
            step = int(self.request.GET.get('step'))
        except (ValueError, TypeError):
            step = 1

        return {'start': start, 'end': end, 'step': step}


class KabNumeralAPIDetailView(generics.RetrieveAPIView):
    serializer_class = KabNaturalNumberSerializer
    queryset = KabNaturalNumber.objects.all()

    @method_decorator(cache_page(CACHE_24_HOURS))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
