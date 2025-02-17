from votes.models import Vote
from rest_framework.exceptions import ValidationError


def validate_user_vote(user, menu):
    """
    Validate that the user has not already voted for the given menu.
    """
    if Vote.objects.filter(user=user, menu=menu).exists():
        raise ValidationError("You have already voted for this menu.")
