from django.urls import path
from rest_framework import routers
from . import api

app_name = 'kab_rus_dictionary'

router = routers.DefaultRouter()
router.register(r'kab-rus-dictionary/categories', api.CategoryViewSet, basename='categories')
router.register(r'kab-rus-dictionary', api.KabRusDictionaryViewSet, basename='kab_rus_dictionary')

urlpatterns = [
    path(r'kab-rus-dictionary/telegram/', api.KabRusDictionaryTelegramAPIListView.as_view()),
    path(r'kab-rus-dictionary/random-kab-word/', api.RandomKabWordApiView.as_view()),
    path(r'kab-rus-dictionary/all/', api.KabRusDictionaryAllAPIView.as_view()),
]

urlpatterns += router.urls
