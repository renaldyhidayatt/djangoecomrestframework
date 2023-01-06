from django.db import models
from apps.shared.models import TimeStampedModel
from apps.product.models import Product
from apps.users.models import User


# Create your models here.
class Comment(TimeStampedModel):
    content = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(
        Product,
        related_name="comments",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
    )
