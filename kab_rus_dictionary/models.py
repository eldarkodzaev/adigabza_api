from django.db import models
from django.contrib.postgres.fields import IntegerRangeField
from django.template.defaultfilters import truncatewords

from rest_framework.reverse import reverse

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from kab_alphabet.models import KabLetter
from .textutils import normalize_string


class Dialect(models.Model):
    """
    Диалект (говор) к которому относится слово.
    """
    dialect_rus = models.CharField(max_length=20)
    dialect_kab = models.CharField(max_length=30)

    class Meta:
        ordering = ('dialect_rus',)
        unique_together = ('dialect_rus', 'dialect_kab',)

    def __str__(self) -> str:
        return self.dialect_rus

    @classmethod
    def get_default_dialect(cls):
        dialect, created = cls.objects.get_or_create(
            dialect_rus='баксанский', dialect_kab='бахъсэн')
        return dialect.pk


class KabWord(models.Model):
    """
    Модель слова
    """
    word = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    letter = models.ForeignKey(KabLetter, on_delete=models.PROTECT, related_name='words')
    borrowed_from = models.ForeignKey('Language', on_delete=models.SET_DEFAULT,
                                      null=True, blank=True, default=None, related_name='words')
    dialect = models.ForeignKey('Dialect',
                                on_delete=models.SET_DEFAULT, default=Dialect.get_default_dialect)
    synonyms = models.ManyToManyField('self', blank=True)

    class Meta:
        ordering = ('letter__id', 'word',)

    def __str__(self) -> str:
        return self.word

    def get_absolute_url(self) -> str:
        url = reverse('kab_rus_dictionary:kab_rus_dictionary-detail', kwargs={'slug': self.slug})
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
    part_of_speech = models.ForeignKey('PartOfSpeech', on_delete=models.SET_DEFAULT,
                                       related_name='words', null=True, blank=True, default=None)
    source = models.ForeignKey('Source', on_delete=models.SET_DEFAULT,
                               related_name='words', null=True, blank=True, default=None)

    class Meta:
        ordering = ('word__letter__id', 'word',)

    def __str__(self) -> str:
        return f"{self.word.word} | {truncatewords(self.translation, 3)}"

    def save(self, *args, **kwargs):
        self.translation = normalize_string(self.translation)
        if self.description:
            self.description = normalize_string(self.description)
        super().save(*args, **kwargs)


class Category(MPTTModel):
    """
    Модель категории, к которой относится слово
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    translation_kab = models.CharField(max_length=255, null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ('name',)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        url = reverse('kab_rus_dictionary:categories-detail', kwargs={'slug': self.slug})
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

    def __str__(self) -> str:
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

    def __str__(self) -> str:
        return self.name


class Language(models.Model):
    """
    Модель языка. Используется для указания факта заимствования слова из этого языка.
    """
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Life(models.Model):
    """
    Как адыги делили человеческую жизнь
    """
    ages = IntegerRangeField()
    description_kab = models.TextField()
    description_rus = models.TextField()

    def __str__(self) -> str:
        return f"{self.ages}"


class Proverb(models.Model):
    """
    Пословица
    """
    word = models.ForeignKey('KabWord', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    translation = models.TextField()

    def __str__(self) -> str:
        return truncatewords(self.text, 3)


class ExampleOfUseKabWord(models.Model):
    """
    Пример употребления слова KabWord
    """
    word = models.ForeignKey('KabWord', on_delete=models.CASCADE, related_name='examples')
    example = models.CharField(max_length=255)
    translation = models.TextField()

    def __str__(self) -> str:
        return self.word.word


class KabWordRelatedPhrases(models.Model):
    """
    Связанные с KabWord фразы
    """
    phrase = models.CharField(max_length=100)
    translation = models.TextField()
    word = models.ForeignKey('KabWord', on_delete=models.CASCADE, related_name='phrases')

    def __str__(self) -> str:
        return self.word.word
