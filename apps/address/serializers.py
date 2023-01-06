from rest_framework import serializers

from .models import Address
from apps.users.serializers import UsernameAndIdSerializer


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = [
            "id",
            "first_name",
            "last_name",
            "address",
            "city",
            "county",
            "zip_code",
            "user",
        ]

    def get_user(self, address):
        if self.context.get("include_user", False):
            return UsernameAndIdSerializer(address.user).data

    def to_representation(self, instance):
        response = super(AddressSerializer, self).to_representation(instance)

        if response.get("user") is None:
            response.pop("user")

        return response

    def create(self, validate_data):
        return Address.objects.create(user=self.context.get("user"), **validate_data)
