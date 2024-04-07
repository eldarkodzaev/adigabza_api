from rest_framework import routers

from . import api

app_name = 'kab_alphabet'

router = routers.DefaultRouter()
router.register(r'kab-alphabet', api.KabAlphabetViewset, basename='kab_alphabet')

urlpatterns = router.urls
