from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import KabWord, Translation, Category, PartOfSpeech, Language, Source
from kab_alphabet.serializers import KabLetterSerializer


class KabWordBorrowedFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class PartOfSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartOfSpeech
        fields = '__all__'


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = '__all__'


class TranslationSerializer(serializers.ModelSerializer):
    part_of_speech = PartOfSpeechSerializer(read_only=True)
    source = SourceSerializer(read_only=True)
    
    class Meta:
        model = Translation
        fields = ['translation', 'description', 'part_of_speech', 'source']


class KabWordSerializer(serializers.ModelSerializer):
    letter = KabLetterSerializer(read_only=True)
    borrowed_from = KabWordBorrowedFromSerializer(read_only=True)
    translations = TranslationSerializer(read_only=True, many=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = KabWord
        fields = ['id', 'word', 'letter', 'slug', 'borrowed_from', 'translations', 'url']
        lookup_field = 'slug'


class TranslationAndDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['translation', 'description']


class KabWordTelegramSerializer(serializers.ModelSerializer):
    translations = TranslationAndDescriptionSerializer(read_only=True, many=True)

    class Meta:
        model = KabWord
        fields = ['word', 'translations']
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'url', 'translation_kab', 'description', 'children']


class TranslationWithCategorySerializer(serializers.ModelSerializer):
    part_of_speech = PartOfSpeechSerializer(read_only=True)
    source = SourceSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Translation
        fields = ['translation', 'description', 'part_of_speech', 'source', 'categories']


class KabWordWithURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = KabWord
        fields = ['word', 'url']


class TranslationWithKabWordSerializer(serializers.ModelSerializer):
    word = serializers.StringRelatedField()

    class Meta:
        model = Translation
        fields = ['word', 'translation']


class KabWordWithCategorySerializer(serializers.ModelSerializer):
    translations = TranslationWithCategorySerializer(read_only=True, many=Translation)
    borrowed_from = KabWordBorrowedFromSerializer(read_only=True)
    
    class Meta:
        model = KabWord
        fields = ['word', 'slug', 'letter', 'borrowed_from', 'translations']


class TranslationForRandomKabWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['translation', 'description']


class RandomKabWordSerializer(serializers.ModelSerializer):
    translations = TranslationForRandomKabWordSerializer(read_only=True, many=True)

    class Meta:
        model = KabWord
        fields = ['word', 'translations']


class TranslationOnlyTranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ['translation']


class KabWordAndTranslationOnlySerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='get_absolute_url', read_only=True)
    translations = TranslationOnlyTranslationSerializer(read_only=True, many=True)

    class Meta:
        model = KabWord
        fields = ['word', 'url', 'translations']