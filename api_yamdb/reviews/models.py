from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=64)
    year = models.PositiveSmallIntegerField()
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=timezone.now().year),
                name='year_lte_now'
            )
        ]


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.PositiveSmallIntegerField("Оценка", default=0)
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)
