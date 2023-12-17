from django.urls import path
from .api import (
    KabRusDictionaryAPIListView, KabWordAPIDetailView, RandomKabWordAPIDetailView,
    CategoryAPIView, CategoriesListAPIView,
)

app_name = 'kab_rus_dictionary'

urlpatterns = [
    path('kab-rus-dictionary/', KabRusDictionaryAPIListView.as_view(), name='kab_rus_dictionary'),
    path('kab-rus-dictionary/random/', RandomKabWordAPIDetailView.as_view(), name='kab_word_random'),
    path('kab-rus-dictionary/categories/', CategoriesListAPIView.as_view(), name='categories'),
    path('kab-rus-dictionary/category/<slug:slug>/', CategoryAPIView.as_view(), name='category'),
    path('kab-rus-dictionary/<slug:slug>/', KabWordAPIDetailView.as_view(), name='kab_word_detail'),
]
