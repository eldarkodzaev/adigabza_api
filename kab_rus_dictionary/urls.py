from django.urls import path
from .views import KabRusDictionaryAPIListView, KabWordAPIDetailView

app_name = 'kab_rus_dictionary'

urlpatterns = [
    path('kab-rus-dictionary/', KabRusDictionaryAPIListView().as_view(), name='kab_rus_dictionary'),
    path('kab-rus-dictionary/<slug:slug>/', KabWordAPIDetailView.as_view(), name='kab_word_detail'),
]
