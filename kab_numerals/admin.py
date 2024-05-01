from django.contrib import admin

from .models import KabNaturalNumber


@admin.register(KabNaturalNumber)
class KabNaturalNumberAdmin(admin.ModelAdmin):
    list_display = ['number', 'translate_decimal']
