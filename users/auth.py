from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from users.models import UniversityUser


class UniversityUserTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        university_user = UniversityUser.objects.filter(pk=user.pk).first()
        return (university_user or user), token


class UniversityUserSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        user_auth = super().authenticate(request)
        if user_auth is None:
            return user_auth

        user, auth = user_auth
        university_user = UniversityUser.objects.filter(pk=user.pk).first()
        return (university_user or user), auth
