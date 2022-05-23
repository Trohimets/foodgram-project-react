from django.db import models
from django.contrib.auth.models import AbstractUser


USER = "user"
ADMIN = "admin"
ROLES = [
    ("user", USER),
    ("admin", ADMIN)
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    role = models.CharField(
        max_length=max(len(role) for _, role in ROLES),
        choices=ROLES,
        default=USER
    )
