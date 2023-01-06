import os
import re
from random import choice
from string import ascii_lowercase

from django.db.models import Count
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from apps.categories.models import Category
from apps.fileupload.models import ProductImage
from .models import Product
from .serializers import ProductListSummarySerializer, ProductDetailsSerializer
from apps.shared.renders import AppJsonRenderer
from apps.tags.models import Tag


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSummarySerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = self.queryset.order_by("-created_at")
        queryset = queryset.annotate(Count("comments"))
        return queryset

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context["request"] = request
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(
            page, many=True, context=serializer_context
        )
        return self.get_paginated_response(serialized_data.data)

    def get_renderer_context(self):
        renderer_context = super(ProductListView, self).get_renderer_context()
        renderer_context["paginator"] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name="products")]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            "request": request,
            "include_urls": True,
        }
        tags = []
        categories = []
        for header_key in list(request.data.keys()):
            if "tags[" in header_key:
                name = header_key[header_key.find("[") + 1 : header_key.find("]")]
                description = request.data[header_key]
                tag, created = Tag.objects.get_or_create(
                    name=name, defaults={"description": description}
                )
                tags.append(tag)

            if header_key.startswith("categories["):
                result = re.search("\[(.*?)\]", header_key)
                if len(result.groups()) == 1:
                    name = result.group(1)
                    description = request.data[header_key]
                    category, created = Category.objects.get_or_create(
                        name=name, defaults={"description": description}
                    )
                    categories.append(category)
        images = request.data.getlist("images[]")

        dir = os.path.join(os.getcwd(), "static", "images", "products")
        file_name = "".join(choice(ascii_lowercase) for i in range(16)) + ".png"

        if not os.path.exists(dir):
            os.makedirs(dir)

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )

        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        product.tags.add(*tags)
        product.categories.add(*categories)

        for image in images:
            file_path = os.path.join(dir, file_name)
            with open(file_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                    ProductImage.objects.create(
                        file_name=file_name,
                        original_name=image.name,
                        file_length=image.size,
                        product=product,
                        file_path=file_path.replace(os.getcwd(), "").replace("\\", "/"),
                    )

        data = {"full_messages": ["Product created successfully"]}
        data.update(ProductDetailsSerializer(product, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)


class ProductDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    renderer_classes = (AppJsonRenderer,)

    def get_queryset(self):
        if self.kwargs.get("pk", None) is not None:
            return Product.objects.filter(pk=self.kwargs["pk"])
        else:
            return Product.objects.filter(slug=self.kwargs["slug"])

    def get_serializer_context(self):
        context = super(ProductDetailsView, self).get_serializer_context()
        context["include_user"] = True
        context["include_product"] = False
        return context

    @property
    def lookup_field(self):
        if self.kwargs.get("pk", None) is not None:
            return "pk"
        else:
            return "slug"
