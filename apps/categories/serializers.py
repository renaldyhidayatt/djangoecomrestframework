import os
from random import choice
from string import ascii_lowercase
from rest_framework import serializers
from apps.fileupload.models import CategoryImage

from .models import Category


class CategoryIdAndNameSerializer(serializers.ModelSerializer):
    image_urls = serializers.SerializerMethodField()

    def get_image_urls(self, category):
        if self.context.get("include_urls", False):
            return [x.file_path for x in category.images.all()]

        return None

    def to_representation(self, instance):
        response = super(CategoryIdAndNameSerializer, self).to_representation(instance)
        if response.get("image_urls") is None:
            response.pop("image_urls")

        return response

    def create(self, validated_data):
        request = self.context["request"]
        images = request.data.getlist("images")

        dir = os.path.join(os.getcwd(), "static", "images", "categories")
        file_name = "".join(choice(ascii_lowercase) for i in range(16)) + ".png"

        if not os.path.exists(dir):
            os.makedirs(dir)

        category = super(CategoryIdAndNameSerializer, self).create(validated_data)

        for image in images:
            file_path = os.path.join(dir, file_name + ".png")
            with open(file_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                    CategoryImage.objects.create(
                        file_name=file_name,
                        original_name=image.name,
                        file_length=image.size,
                        category=category,
                        file_path=file_path.replace(os.getcwd(), "").replace("\\", "/"),
                    )

        return category

    class Meta:
        model = Category
        fields = ["id", "name", "image_urls"]
