from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class CustomUser(AbstractBaseUser):

    ROLE_OPTIONS = (
        (1, 'user'),
        (2, 'moderator'),
        (3, 'admin'),
    )

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField()
    role = models.CharField(max_length=10, choices=ROLE_OPTIONS, default=1)
    confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
