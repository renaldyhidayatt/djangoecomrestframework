from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentSerializer
from apps.product.models import Product
from apps.shared.renders import AppJsonRenderer


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(product__slug=self.kwargs["slug"])

    def list(self, request, *args, **kwargs):
        serializer_context = self.get_serializer_context()
        serializer_context["request"] = request
        page = self.paginate_queryset(self.get_queryset())
        serialized_data = self.serializer_class(
            page, many=True, context=serializer_context
        )
        return self.get_paginated_response(serialized_data.data)

    def get_serializer_context(self):
        serializer_context = super(CommentListView, self).get_serializer_context()
        serializer_context["include_user"] = True
        serializer_context["include_product"] = False
        return serializer_context

    def get_renderer_context(self):
        renderer_context = super(CommentListView, self).get_renderer_context()
        renderer_context["paginator"] = self.paginator
        return renderer_context

    def get_renderers(self):
        return [AppJsonRenderer(resources_name="comments")]

    def create(self, request, *args, **kwargs):
        serializer_context = {
            "user": request.user,
            "request": request,
            "include_user": True,
            "include_product": True,
        }

        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(slug=kwargs["slug"])
        serializer_context["product"] = product
        comment = serializer.save()
        data = {"full_messages": ["Comment created successfully"]}

        data.update(CommentSerializer(comment, context=serializer_context).data)
        return Response(data, status=status.HTTP_201_CREATED)


class CommentsDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    renderer_classes = (AppJsonRenderer,)
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs["pk"])

    def get_serializer_context(self):
        context = super(CommentsDetailsView, self).get_serializer_context()
        context["include_user"] = True
        context["include_product"] = True
        return context

    def destroy(self, request, *args, **kwargs):
        response = super(CommentsDetailsView, self).destroy(request, args, kwargs)
        return Response(
            {"full_messages": ["Removed comment successfully"]},
            status=status.HTTP_204_NO_CONTENT,
        )
