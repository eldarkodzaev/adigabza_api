from django.db import models


class KabNaturalNumber(models.Model):
    """
    Модель натуральных чисел
    """
    number = models.PositiveIntegerField(primary_key=True)
    translate_decimal = models.CharField(max_length=128)  # в 10-й системе счисления

    class Meta:
        ordering = ('number',)

    def __str__(self):
        return f'{self.number}'
