from django.db import models
from .settings import URL


class KabLetter(models.Model):
    letter = models.CharField(max_length=4, unique=True, db_index=True)
    slug = models.SlugField(max_length=4, unique=True, db_index=True, allow_unicode=True)
    is_vowel = models.BooleanField()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.letter

    def get_absolute_url(self):
        return f'/{URL}{self.slug}/'
