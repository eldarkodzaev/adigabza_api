from django.urls import path
from .views import KabNumeralsAPIListView, KabNumeralAPIDetailView

app_name = 'kab_numerals'

urlpatterns = [
    path('kab-numerals/', KabNumeralsAPIListView.as_view(), name='kab_numerals'),
    path('kab-numerals/<int:pk>/', KabNumeralAPIDetailView.as_view(), name='kab_numerals_detail'),
]
