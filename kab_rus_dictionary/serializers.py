from rest_framework import serializers

from .models import KabWord, Translation, Category, PartOfSpeech, Language


class KabWordSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = KabWord
        fields = ['word', 'slug', 'letter', 'borrowed_from', 'url']
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'lft', 'rght', 'tree_id', 'level', 'parent', 'url']
        lookup_field = 'slug'


class TranslationSerializer(serializers.ModelSerializer):
    word = KabWordSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Translation
        fields = ['word', 'categories', 'translation', 'description']


class PartOfSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartOfSpeech
        fields = '__all__'


class KabRusDictionarySerializer(serializers.ModelSerializer):
    word = KabWordSerializer(read_only=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Translation
        fields = '__all__'


class KabTranslationSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    part_of_speech = PartOfSpeechSerializer()

    class Meta:
        model = Translation
        fields = ['translation', 'description', 'part_of_speech', 'categories']


class KabWordBorrowedFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class KabWordDetailSerializer(serializers.ModelSerializer):
    translations = KabTranslationSerializer(many=True)
    borrowed_from = KabWordBorrowedFromSerializer()

    class Meta:
        model = KabWord
        fields = ['word', 'borrowed_from', 'translations']


class RandomKabWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KabWord
        fields = ['word']
