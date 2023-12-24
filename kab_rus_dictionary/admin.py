from django.contrib import admin
from django.template.defaultfilters import truncatewords

from .models import KabWord, Translation, Category, PartOfSpeech, Source, Language


class TranslationInline(admin.StackedInline):
    model = Translation


@admin.register(KabWord)
class KabWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'slug', 'letter', 'borrowed_from']
    list_filter = ['letter']
    search_fields = ['word']
    inlines = [TranslationInline]


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ['word', 'get_translation', 'get_description']
    search_fields = ['word__word']

    def get_translation(self, obj):
        return truncatewords(obj.translation, 10)

    def get_description(self, obj):
        return truncatewords(obj.description, 10)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PartOfSpeech)
class PartOfSpeechAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'year', 'url']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']
