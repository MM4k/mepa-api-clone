from rest_framework import exceptions

from utils.user.user_type_util import UserType

from . import models


class RequestsPermissions:
    default_users_permissions = [
        models.CustomUser.super_user_type,
        models.CustomUser.university_admin_user_type,
        models.CustomUser.university_user_type,
    ]

    super_user_permissions = [models.CustomUser.super_user_type]
    admin_permission = [models.CustomUser.super_user_type, models.CustomUser.university_admin_user_type]
    university_admin_user_permissions = [models.CustomUser.university_admin_user_type]

    university_user_permissions = [
        models.CustomUser.university_admin_user_type,
        models.CustomUser.university_user_type,
    ]

    def check_request_permissions(request_user, user_types_with_permission, request_university_id=None):
        user_type = UserType.get_user_type(request_user.type)
        user_has_permission = RequestsPermissions.check_type_user_has_permission(user_type, user_types_with_permission)

        if user_has_permission and (user_type in RequestsPermissions.university_user_permissions):
            user_has_permission = RequestsPermissions.check_university_user_has_permissions(
                request_university_id, request_user.id
            )

        if not user_has_permission:
            raise PermissionsException.user_has_not_permission_exception()

    def check_type_user_has_permission(user_type, user_types_with_permission):
        if user_type in user_types_with_permission:
            return True

        return False

    def check_university_user_has_permissions(request_university_id, user_id):
        if not request_university_id:
            raise PermissionsException.request_university_id_is_necessary_exception()

        university_user = RequestsPermissions.get_university_user_object(user_id)
        return int(request_university_id) == int(university_user.university.id)

    def get_university_user_object(user_university_id):
        return models.UniversityUser.objects.get(id=user_university_id)


class PermissionsException:
    def request_university_id_is_necessary_exception():
        raise exceptions.AuthenticationFailed("University id is necessary.")

    def user_has_not_permission_exception():
        raise exceptions.AuthenticationFailed("This User does not have permission.")
