from rest_framework import serializers

from kab_alphabet.models import KabLetter


class KabLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KabLetter
        fields = '__all__'
        lookup_field = 'slug'
