from datetime import datetime
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from apps.shared.models import TimeStampedModel
from apps.tags.models import Tag
from apps.categories.models import Category


# Create your models here.
class Product(TimeStampedModel):
    name = models.CharField(blank=False, null=False, max_length=200)
    slug = models.CharField(blank=False, null=False, max_length=100)
    description = models.TextField(blank=False, null=False)
    price = models.FloatField(validators=[MinValueValidator(0.1)])
    publish_on = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="tag")
    categories = models.ManyToManyField(Category, related_name="category")

    stock = models.IntegerField(validators=[MinValueValidator(0)])

    def save(self, slug="", *args, **kwargs):
        if not self.publish_on:
            self.publish_on = datetime.now()

        if not self.slug:
            self.slug = slugify(self.name)

        return super(Product, self).save(*args, **kwargs)
