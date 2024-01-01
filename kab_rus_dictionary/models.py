from django.db import models
from django.contrib.postgres.fields import IntegerRangeField
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from kab_alphabet.models import KabLetter
from .utils import normalize_string


class KabWord(models.Model):
    """
    Модель слова
    """
    word = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    letter = models.ForeignKey(KabLetter, on_delete=models.PROTECT, related_name='words')
    borrowed_from = models.ForeignKey('Language', on_delete=models.SET_DEFAULT, null=True, blank=True, default=None,
                                      related_name='words')

    class Meta:
        ordering = ('letter__id', 'word',)

    def __str__(self):
        return self.word

    def get_absolute_url(self):
        url = reverse('kab_rus_dictionary:kab_word_detail', kwargs={'slug': self.slug})
        return url[url.find('kab-rus-dictionary') - 1:]

    def save(self, *args, **kwargs):
        if (first_letter := self.word[0]) != 'I':
            self.word = first_letter.lower() + self.word[1:]
        super().save(*args, **kwargs)


class Translation(models.Model):
    """
    Модель хранящая перевод, описание и прочую информацию о слове
    """
    translation = models.TextField()
    description = models.TextField(null=True, blank=True)

    word = models.ForeignKey(KabWord, on_delete=models.CASCADE, related_name='translations')
    categories = models.ManyToManyField('Category', blank=True, default=None)
    part_of_speech = models.ForeignKey('PartOfSpeech', on_delete=models.SET_DEFAULT, related_name='words', null=True,
                                       blank=True, default=None)
    source = models.ForeignKey('Source', on_delete=models.SET_DEFAULT, related_name='words', null=True, blank=True,
                               default=None)

    class Meta:
        ordering = ('word__letter__id', 'word',)

    def __str__(self):
        return f"{self.word.word} | {truncatewords(self.translation, 3)}"

    def save(self, *args, **kwargs):
        self.translation = normalize_string(self.translation)
        if self.description:
            self.description = normalize_string(self.description)
        super().save(*args, **kwargs)


class CategoryManager(TreeManager):
    def viewable(self):
        queryset = self.get_queryset().filter(level=0)
        return queryset


class Category(MPTTModel):
    """
    Модель категории, к которой относится слово
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    translation_kab = models.CharField(max_length=255, null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ('name',)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url = reverse('kab_rus_dictionary:category', kwargs={'slug': self.slug})
        return url[url.find('kab-rus-dictionary') - 1:]


class PartOfSpeech(models.Model):
    """
    Модель части речи, к которой относится слово
    """
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)
        verbose_name = 'part of speech'
        verbose_name_plural = 'parts of speech'

    def __str__(self):
        return self.name


class Source(models.Model):
    """
    Модель источника информации определенного слова
    """
    name = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    year = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Модель языка. Используется для указания факта заимствования слова из этого языка.
    """
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Life(models.Model):
    """
    Как адыги делили человеческую жизнь
    """
    ages = IntegerRangeField()
    description_kab = models.TextField()
    description_rus = models.TextField()

    def __str__(self):
        return f"{self.ages}"
