from rest_framework.permissions import BasePermission
from restaurants.models import Restaurant


class IsMenuOwner(BasePermission):
    """
    Permission to check if the user is the owner of the menu's restaurant.
    """

    def has_object_permission(self, request, view, obj):
        return obj.restaurant.owner == request.user
