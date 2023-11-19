from rest_framework import serializers

from .models import KabWord, Translation, Category


class KabWordSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = KabWord
        fields = ['word', 'slug', 'letter', 'borrowed_from', 'url']
        lookup_field = 'slug'


class KabRusDictionarySerializer(serializers.ModelSerializer):
    word = KabWordSerializer(read_only=True)

    class Meta:
        model = Translation
        fields = '__all__'


class KabTranslationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Translation
        fields = ['translation', 'description', 'part_of_speech', 'categories']


class KabWordDetailSerializer(serializers.ModelSerializer):
    translations = KabTranslationSerializer(many=True)

    class Meta:
        model = KabWord
        fields = ['word', 'borrowed_from', 'translations']


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'
