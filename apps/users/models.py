from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from apps.shared.models import TimeStampedModel
from .manager import MyUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator],
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )
    email = models.EmailField(blank=False, unique=True)
    is_staff = models.BooleanField(
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )

    object = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
