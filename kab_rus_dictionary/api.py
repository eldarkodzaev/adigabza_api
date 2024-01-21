from rest_framework import viewsets, generics
from rest_framework.response import Response

from .models import KabWord, Category, Translation
from .serializers import (
    KabWordSerializer, CategorySerializer, RandomKabWordSerializer,
    KabWordWithCategorySerializer, TranslationWithKabWordSerializer,
    KabWordTelegramSerializer,
)


class KabRusDictionaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KabWord.objects.select_related(
        'letter', 'borrowed_from').prefetch_related(
            'translations', 'translations__part_of_speech', 'translations__source')
    serializer_class = KabWordSerializer
    lookup_field = 'slug'
    
    def list(self, request, *args, **kwargs):
        if word := request.GET.get('word'):
            queryset = self.queryset.filter(word__istartswith=word)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        word_instance = self.get_object()
        word_serializer = KabWordWithCategorySerializer(word_instance, context={'request': request})
        return Response(word_serializer.data)


class KabRusDictionaryAllAPIView(generics.ListAPIView):
    queryset = KabWord.objects.select_related(
        'letter').prefetch_related(
            'translations', 'translations__part_of_speech', 'translations__source')
    serializer_class = KabWordSerializer
    pagination_class = None
    lookup_field = 'slug'


class KabRusDictionaryTelegramAPIListView(generics.ListAPIView):
    serializer_class = KabWordTelegramSerializer
    
    def get_queryset(self):
        if word := self.request.GET.get('word'):
            return KabWord.objects.prefetch_related('translations').filter(word__istartswith=word)[:10]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(level=0).prefetch_related('children__children__children__children')
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        try:
            category_instance = Category.objects.prefetch_related(
                'children__children__children__children'
            ).get(slug=kwargs['slug'])
        except Category.DoesNotExist:
            return super().retrieve(request, *args, **kwargs)
        category_serializer = CategorySerializer(category_instance, context={'request': request})
        translations_for_this_category = Translation.objects.prefetch_related(
            'word', 'categories').filter(categories=category_instance)
        translations_serializer = TranslationWithKabWordSerializer(translations_for_this_category, many=True)
        return Response({
            'category': category_serializer.data,
            'translations': translations_serializer.data,
        })


class RandomKabWordApiView(generics.RetrieveAPIView):
    serializer_class = RandomKabWordSerializer

    def get_object(self):
        random_word = KabWord.objects.prefetch_related('translations').order_by('?').first()
        return random_word
    