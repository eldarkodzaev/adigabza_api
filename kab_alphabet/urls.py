from django.urls import path, include
from rest_framework import routers
from .views import KabAlphabetViewset

app_name = 'kab_alphabet'

router = routers.DefaultRouter()
router.register(r'kab-alphabet', KabAlphabetViewset, basename='kab_alphabet')

urlpatterns = [
    path('', include(router.urls))
]
