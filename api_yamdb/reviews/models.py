from django.db import models


class User(models.Model):
    USER = 'USR'
    MODERATOR = 'MOD'
    ADMIN = 'ADM'
    ROLE_CHOICES =[
        (USER , 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]
    username = models.CharField(max_length=200) # поставить ограничение в Serializer на имя "me"
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=3,
        choices=ROLE_CHOICES,
        default=USER,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user'
            ),
        )
