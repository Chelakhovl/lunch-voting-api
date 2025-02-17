from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permission to check if the user is a restaurant admin.
    """

    def has_permission(self, request, view):
        return request.user.role == "restaurant_admin"
