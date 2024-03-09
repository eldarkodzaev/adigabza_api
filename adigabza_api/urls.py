"""
URL configuration for adigabza_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .settings.base import API_PATH


urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PATH, include('kab_rus_dictionary.urls', namespace='kab_rus_dictionary')),
    path(API_PATH, include('kab_numerals.urls', namespace='kab_numerals')),
    path(API_PATH, include('kab_alphabet.urls', namespace='kab_alphabet')),
    path("__debug__/", include("debug_toolbar.urls")),
]
