from rest_framework import permissions


class UniversityPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        return obj == request.user.university


class ConsumerUnitPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous or request.user.is_admin:
            return False

        if request.user.university is None:
            return False

        if request.user.is_guest:
            return request.method in permissions.SAFE_METHODS

        return True

    def has_object_permission(self, request, view, obj):
        return obj.university.id == request.user.university.id
