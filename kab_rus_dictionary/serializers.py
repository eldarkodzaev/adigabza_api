from rest_framework import serializers

from .models import KabWord, Translation, Category, PartOfSpeech


class KabWordSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = KabWord
        fields = ['word', 'slug', 'letter', 'borrowed_from', 'url']
        lookup_field = 'slug'


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class PartOfSpeechSerializer(serializers.ModelSerializer):

    class Meta:
        model = PartOfSpeech
        fields = '__all__'


class KabRusDictionarySerializer(serializers.ModelSerializer):
    word = KabWordSerializer(read_only=True)
    categories = CategoryDetailSerializer(many=True)

    class Meta:
        model = Translation
        fields = '__all__'


class KabTranslationSerializer(serializers.ModelSerializer):
    categories = CategoryDetailSerializer(many=True)
    part_of_speech = PartOfSpeechSerializer()

    class Meta:
        model = Translation
        fields = ['translation', 'description', 'part_of_speech', 'categories']


class KabWordDetailSerializer(serializers.ModelSerializer):
    translations = KabTranslationSerializer(many=True)

    class Meta:
        model = KabWord
        fields = ['word', 'borrowed_from', 'translations']
