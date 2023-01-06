from rest_framework import serializers, fields
from .models import Comment
from apps.users.serializers import UsernameAndIdSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "user", "product"]

    def get_product(self, comment):
        if self.context.get("include_product", False):
            pass
        else:
            return None

    def get_user(self, comment):
        pass

    def to_representation(self, instance):
        response = super(CommentSerializer, self).to_representation(instance)
        if response.get("product") is None:
            response.pop("product")

        if response.get("user") is None:
            response.pop("user")

        return response

    def create(self, validated_data):
        comment = Comment.objects.create(
            content=validated_data["content"],
            user=self.context["user"],
            product=self.context["product"],
        )
        return comment
