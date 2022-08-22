from django.contrib.auth import get_user_model

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Жанр")
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Имя ссылки"
    )

    class Meta:
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="Категория")
    slug = models.SlugField(
        max_length=50, unique=True, verbose_name="Имя ссылки"
    )

    class Meta:
        ordering = ["name"]


class Title(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название")
    year = models.PositiveSmallIntegerField(verbose_name="Год выхода")
    rating = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="Рейтинг"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )
    genre = models.ManyToManyField(
        Genre, through="GenreTitle", related_name="titles", verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Категория",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(year__lte=timezone.now().year),
                name="year_lte_now",
            )
        ]
        ordering = ["name"]

    @property
    def rating(self):
        return self.reviews.aggregate(Avg("score"))["score__avg"]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name="Название"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name="Жанр"
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_constraint=False,
        verbose_name="Название",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        error_messages={"validators": "От одного до десяти!"},
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата добавления"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique author review"
            )
        ]

        ordering = ["-pub_date"]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Ревью",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Дата добавления"
    )

    class Meta:
        ordering = ["-pub_date"]
