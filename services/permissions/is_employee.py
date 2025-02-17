from rest_framework.permissions import BasePermission


class IsEmployee(BasePermission):
    """
    Permission to check if the user is an employee.
    """

    def has_permission(self, request, view):
        return request.user.role == "employee"
