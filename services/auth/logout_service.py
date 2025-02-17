from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError


def blacklist_refresh_token(refresh_token: str):
    """
    Blacklist a refresh token if it's valid.
    """
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        raise ValidationError("Invalid or expired refresh token")
