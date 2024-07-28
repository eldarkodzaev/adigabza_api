from django.contrib import admin
from django.template.defaultfilters import truncatewords

from .models import (
    KabWord, Translation, Category,
    PartOfSpeech, Source, Language,
    Life, Dialect, Proverb,
    ExampleOfUseKabWord, KabWordRelatedPhrases
)


class TranslationInline(admin.StackedInline):
    model = Translation
    filter_horizontal = ['categories']


@admin.register(KabWord)
class KabWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'slug', 'letter', 'borrowed_from', 'dialect']
    list_filter = ['letter']
    search_fields = ['word']
    inlines = [TranslationInline]
    prepopulated_fields = {'slug': ('word',)}
    filter_horizontal = ['synonyms']


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ['word', 'get_translation', 'get_description']
    search_fields = ['word__word']
    filter_horizontal = ['categories']

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


@admin.register(Life)
class LifeAdmin(admin.ModelAdmin):
    list_display = ['ages', 'get_description_rus', 'get_description_kab']

    def get_description_rus(self, obj):
        return truncatewords(obj.description_rus, 10)

    def get_description_kab(self, obj):
        return truncatewords(obj.description_kab, 10)


@admin.register(Dialect)
class DialectAdmin(admin.ModelAdmin):
    list_display = ['dialect_rus', 'dialect_kab']


@admin.register(Proverb)
class ProverbAdmin(admin.ModelAdmin):
    list_display = ['word', 'text']


@admin.register(ExampleOfUseKabWord)
class ExampleOfUseKabWordAdmin(admin.ModelAdmin):
    list_display = ['word', 'example', 'translation']
    autocomplete_fields = ['word']


@admin.register(KabWordRelatedPhrases)
class KabWordRelatedPhrases(admin.ModelAdmin):
    list_display = ['word', 'phrase']
    autocomplete_fields = ['word']
