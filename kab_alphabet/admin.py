from django.contrib import admin

from .models import KabLetter


@admin.register(KabLetter)
class KabLetterAdmin(admin.ModelAdmin):
    list_display = ['letter', 'slug', 'is_vowel']
