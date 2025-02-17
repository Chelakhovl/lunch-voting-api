from rest_framework.permissions import BasePermission
from restaurants.models import Restaurant


class IsRestaurantOwner(BasePermission):
    """
    Permission to check if the user is the owner of the restaurant.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
