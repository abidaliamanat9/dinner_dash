from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    email = models.EmailField(
        max_length=50,
        unique=True,
        error_messages={
            "unique": ("A user with that email already exists."),
        },
    )
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    display_name = models.CharField(
        max_length=32,
        blank=True,
        null=True,
    )
    username = None
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
