from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

User = get_user_model()


def validate_user_credentials(email: str, password: str):
    """
    Validate user credentials and return JWT tokens if valid.
    """
    user = User.objects.filter(email=email).first()

    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "surname": user.surname,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
            },
        }

    raise ValidationError("Invalid email or password")
