from rest_framework import serializers

from kab_alphabet.models import KabLetter
from kab_rus_dictionary.models import KabWord


class KabLetterSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = KabLetter
        fields = '__all__'
        lookup_field = 'slug'


class KabWordWithSlugSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    
    class Meta:
        model = KabWord
        fields = ['word', 'slug', 'url']


class KabLetterWithWordsSerializer(serializers.ModelSerializer):
    words = KabWordWithSlugSerializer(many=True, read_only=True)

    class Meta:
        model = KabLetter
        fields = ['id', 'letter', 'slug', 'is_vowel', 'words']
        lookup_field = 'slug'
