from rest_framework import generics

from kab_numerals.models import KabNaturalNumber
from kab_numerals.pagination import KabNumeralsPagination
from kab_numerals.serializers import KabNaturalNumberSerializer


class KabNumeralsAPIListView(generics.ListAPIView):
    serializer_class = KabNaturalNumberSerializer
    pagination_class = KabNumeralsPagination

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
