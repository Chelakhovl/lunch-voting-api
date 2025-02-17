from rest_framework.permissions import BasePermission
from votes.models import Vote


class IsNotVoted(BasePermission):
    """
    Permission to check if the user has not already voted for this menu.
    """

    def has_permission(self, request, view):
        menu_id = request.data.get("menu")
        return not Vote.objects.filter(user=request.user, menu_id=menu_id).exists()
