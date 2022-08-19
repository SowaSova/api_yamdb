from reviews.models import Review, Comment

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


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
