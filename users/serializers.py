from rest_framework import serializers
from django.contrib.auth import get_user_model
from services.validation.validate_login import validate_user_credentials
from services.auth.logout_service import blacklist_refresh_token


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for returning user data.
    """

    class Meta:
        model = User
        fields = ["id", "email", "name", "surname", "role", "created_at"]
        read_only_fields = ["id", "created_at"]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "name", "surname", "password", "role"]

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication (login).
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate login credentials and return JWT tokens if valid.
        """
        return validate_user_credentials(data["email"], data["password"])


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logging out users (blacklisting refresh tokens).
    """

    refresh = serializers.CharField()

    def validate_refresh(self, value):
        """
        Validate and blacklist the refresh token.
        """

        blacklist_refresh_token(value)
        return value
