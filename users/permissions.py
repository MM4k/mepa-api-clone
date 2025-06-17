from rest_framework import permissions

from .models import UniversityUser


class UniversityUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user.is_admin:
            return True
        university_user = UniversityUser.objects.get(id=user.id)
        if user.is_manager and university_user.university == obj.university:
            return True
        return user.id == obj.id
