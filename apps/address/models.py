from django.db import models
from apps.users.models import User


# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(
        User,
        related_name="address",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="User",
    )
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(blank=False, max_length=50)
    country = models.CharField(blank=False, max_length=50)
    city = models.CharField(blank=False, max_length=50)
    address = models.CharField(blank=False, max_length=50)
    zip_code = models.CharField(blank=False, max_length=20)
