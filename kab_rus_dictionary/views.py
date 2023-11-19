from rest_framework import generics

from kab_rus_dictionary.models import Translation, KabWord, Category
from kab_rus_dictionary.serializers import KabRusDictionarySerializer, CategoryDetailSerializer, KabWordDetailSerializer


class KabRusDictionaryAPIListView(generics.ListAPIView):
    serializer_class = KabRusDictionarySerializer

    def get_queryset(self):
        word_param = self.request.GET.get('word')
        qs = Translation.objects.select_related('word')
        if word_param:
            return qs.filter(word__word__icontains=word_param)
        return qs.prefetch_related('categories')


class KabWordAPIDetailView(generics.RetrieveAPIView):
    serializer_class = KabWordDetailSerializer
    queryset = KabWord.objects.all()
    lookup_field = 'slug'


class CategoryDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
