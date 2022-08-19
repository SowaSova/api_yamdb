from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
from reviews.models import Category, Genre, Title, Review, Comment
from rest_framework.exceptions import ValidationError
from django.utils import timezone


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_name(self, value):
        if len(value) > 256:
            raise ValidationError(
                'Название не должно быть длиннее 256 символов!')
        return value

    def validate_slug(self, value):
        if len(value) > 50:
            raise ValidationError(
                'Длина слага должна быть не более 50 символов!')
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def validate(self, value):
        if value > timezone.now().year:
            raise ValidationError(
                'Год выхода произведения еще не наступил!')

class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only="True")

    def create(self, validated_data):
        rating = Review.objects.update_or_create(
            author=validated_data.get("author", None),
            movie=validated_data.get("movie", None),
            defaults={"score": validated_data.get("score")},
        )
        return rating

    class Meta:
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only="True")

    class Meta:
        fields = "__all__"
        model = Comment



