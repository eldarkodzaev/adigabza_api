from rest_framework import serializers

from kab_alphabet.models import KabLetter


class KabLetterSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = KabLetter
        fields = '__all__'
        lookup_field = 'slug'
