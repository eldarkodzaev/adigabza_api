from django.urls import path
from .views import KabAlphabetAPIListView, KabLetterAPIDetailView

app_name = 'kab_alphabet'

urlpatterns = [
    path('kab-alphabet/', KabAlphabetAPIListView.as_view(), name='kab_alphabet'),
    path('kab-alphabet/<slug:slug>/', KabLetterAPIDetailView.as_view(), name='kab_alphabet_detail'),
]
