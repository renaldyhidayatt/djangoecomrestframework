from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from .models import User


class UsernameAndIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class RegisterationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.object.all())]
    )
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.object.all())]
    )
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        user = User.object.create_user(**validated_data)
        return user

    def validate_password(self, password):
        password_confirmation = self.context.get("request").data.get(
            "password_confirmation"
        )

        if password != password_confirmation:
            raise serializers.ValidationError(
                "password and password confirmation do not match"
            )

        return password

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "password_confirmation",
        ]
