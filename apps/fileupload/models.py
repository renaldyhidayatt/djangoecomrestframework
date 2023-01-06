from django.db import models
from apps.categories.models import Category
from apps.product.models import Product
from apps.tags.models import Tag
from apps.users.models import User

from polymorphic.models import PolymorphicModel


# Create your models here.
class FileUpload(PolymorphicModel):
    file_name = models.CharField(max_length=120)
    file_path = models.CharField(max_length=250)
    original_name = models.CharField(max_length=120)
    file_length = models.IntegerField()


class TagImage(FileUpload):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="images")


class ProductImage(FileUpload):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )


class CategoryImage(FileUpload):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="images"
    )


class ProfileImage(FileUpload):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="avatars")
