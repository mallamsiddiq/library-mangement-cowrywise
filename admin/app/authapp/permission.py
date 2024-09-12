from rest_framework.permissions import BasePermission

from authapp.models import User


class IsLibraryAdminUser(BasePermission):
    """
    Custom permission to check if the user has a MechanicProfile
    and the profile status is not 'Pending'.
    """
    message  = "Only Admin Permision"

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        user:User = request.user
        return bool(user.is_superuser)
    