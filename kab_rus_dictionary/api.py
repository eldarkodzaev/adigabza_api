from rest_framework import generics

from kab_rus_dictionary.models import Translation, KabWord, Category
from kab_rus_dictionary.pagination import KabRusDictionaryPagination
from kab_rus_dictionary.serializers import KabRusDictionarySerializer, KabWordDetailSerializer, RandomKabWordSerializer, \
    TranslationSerializer, CategorySerializer


class KabRusDictionaryAPIListView(generics.ListAPIView):
    serializer_class = KabRusDictionarySerializer
    pagination_class = KabRusDictionaryPagination

    def get_queryset(self):
        word_param = self.request.GET.get('word')
        qs = Translation.objects.select_related('word')
        if word_param:
            return qs.filter(word__word__startswith=word_param)[:10]
        return qs.prefetch_related('categories')

    def paginate_queryset(self, queryset):
        if self.request.GET.get('page'):
            return super().paginate_queryset(queryset)


class KabWordAPIDetailView(generics.RetrieveAPIView):
    serializer_class = KabWordDetailSerializer
    queryset = KabWord.objects.all()
    lookup_field = 'slug'


class RandomKabWordAPIDetailView(generics.RetrieveAPIView):
    serializer_class = RandomKabWordSerializer

    def get_object(self):
        return KabWord.objects.only('id', 'word').order_by('?').first()


class CategoryAPIView(generics.ListAPIView):
    serializer_class = TranslationSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Translation.objects.select_related('word').prefetch_related('categories').filter(
            categories__slug=self.kwargs['slug'])

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        response.data['category'] = category.name
        return response


class CategoriesListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
