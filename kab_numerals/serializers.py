from rest_framework import serializers

from .models import KabNaturalNumber


class KabNaturalNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = KabNaturalNumber
        fields = ['number', 'translate_decimal']
