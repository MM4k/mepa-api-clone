from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser, UserToken
from utils.email.send_email import (
    send_email_first_access_password,
    send_email_reset_password,
    send_email_reset_password_by_admin,
)
from utils.endpoints_util import EndpointsUtils
from utils.user.authentication import (
    create_token_response,
    create_valid_token_response,
    generate_link_to_reset_password,
    generate_random_password,
)
from utils.user.user_type_util import UserType

from . import serializers
from .requests_permissions import RequestsPermissions


class Authentication(ObtainAuthToken):
    @swagger_auto_schema(responses={200: serializers.AuthenticationTokenSerializerForDocs()})
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]

            if user.account_password_status not in ["OK", "user_reset"]:
                raise Exception("Usuário não pode fazer login no sistema")

            try:
                existing_token = Token.objects.get(user=user)
                existing_token.delete()
            except Token.DoesNotExist:
                pass

            token = Token.objects.create(user=user)
        except Exception as error:
            return Response({"Authentication error": f"{str(error)}"}, status.HTTP_401_UNAUTHORIZED)

        try:
            UserType.is_valid_user_type(user.type)
            response = Authentication._create_and_update_login_response(
                token.key,
                user.id,
                user.email,
                user.first_name,
                user.last_name,
                user.type,
            )

            return Response(response)
        except Exception as error:
            return Response({"Authentication error": f"{str(error)}"}, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        query_serializer=serializers.AuthenticationGetTokenParamsSerializer,
        responses={200: serializers.AuthenticationGetTokenSerializerForDocs()},
    )
    def get(self, request, *args, **kwargs):
        params_serializer = serializers.AuthenticationGetTokenParamsSerializer(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            Token.objects.get(pk=request.data["token"])
            is_valid_token = True
        except ObjectDoesNotExist:
            is_valid_token = False

        response = create_valid_token_response(is_valid_token)

        return Response(response)

    def _invalid_sessions_tokens(user):
        sessions_tokens = Token.objects.filter(user=user)

        if sessions_tokens:
            sessions_tokens.delete()

    def _create_and_update_login_response(token, user_id, user_email, user_first_name, user_last_name, user_type):
        response = create_token_response(token, user_id, user_email, user_first_name, user_last_name, user_type)

        if user_type in RequestsPermissions.university_user_permissions:
            user = RequestsPermissions.get_university_user_object(user_id)
            university_id = user.university.id
            response = Authentication._update_university_user_response(response, university_id)

        return response

    def _update_super_user_response(response):
        return response

    def _update_university_user_response(response, university_id):
        response = Authentication._insert_university_id_on_response(response, university_id)
        return response

    def _insert_university_id_on_response(response, university_id):
        response["user"]["universityId"] = university_id
        return response


class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()

            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Failed to logout: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Password:
    def generate_password_token(user):
        Password._invalid_all_generated_password_tokens(user)
        token = default_token_generator.make_token(user=user)
        UserToken.objects.create(user=user, token=token)

        return token

    def generate_link_to_reset_password(user: str, token: str or None, password_status: str):
        if not token:
            raise Exception("Is necessary a password token")

        Password._get_user_by_token(token)

        return generate_link_to_reset_password(token, user.first_name, password_status)

    def check_password_token_is_valid(user, token):
        return default_token_generator.check_token(user, token)

    def change_user_password(user_new_password, token):
        try:
            user = Password._get_user_by_token(token)
            user.change_user_password_by_reset_password_token(user_new_password, token)
            user.set_account_password_status_to_ok()
            Password._invalid_all_generated_password_tokens(user)
        except Exception as error:
            raise Exception("Change user password: " + str(error))

    def _get_user_by_token(token):
        return UserToken.get_user_by_token(token)

    def _invalid_all_generated_password_tokens(user):
        UserToken.objects.filter(user=user).delete()

    def send_email_reset_password_by_admin(email):
        try:
            user = CustomUser.search_user_by_email(email=email)
            user.account_password_status = "admin_reset"
            user.save()
            user.set_password(generate_random_password())
            Authentication._invalid_sessions_tokens(user)
            token = Password.generate_password_token(user)
            link = Password.generate_link_to_reset_password(user, token, "admin_reset")
            send_email_reset_password_by_admin(user.first_name, user.email, link)
        except Exception as error:
            raise Exception("Send email reset password by admin: " + str(error))

    def send_email_reset_password(email):
        try:
            user = CustomUser.search_user_by_email(email=email)
            user.account_password_status = "user_reset"
            user.save()
            token = Password.generate_password_token(user)
            link = Password.generate_link_to_reset_password(user, token, "user_reset")
            send_email_reset_password(user.first_name, user.email, link)
        except CustomUser.DoesNotExist:
            pass
        except Exception as error:
            raise Exception("Send email reset password: " + str(error))

    def send_email_first_access_password(user):
        try:
            user.account_password_status = "first_access"
            user.save()
            Authentication._invalid_sessions_tokens(user)
            token = Password.generate_password_token(user)
            link = Password.generate_link_to_reset_password(user, token, "first_access")
            send_email_first_access_password(user.first_name, user.university.acronym, user.email, link)
        except Exception as error:
            raise Exception("Send email first access password: " + str(error))


class ResetPasswordByAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_user = request.user

        if request_user.type not in ["super_user", "university_admin"]:
            raise Exception("Esse usuário não tem permissão para executar essa ação")

        user_id = int(request.GET.get("user_id"))
        user_for_reset = CustomUser.search_user_by_id(user_id)

        if request_user.id == user_for_reset.id:
            raise Exception("Utilize o esqueci minha senha")

        Password.send_email_reset_password_by_admin(user_for_reset.email)

        return Response({"message": "Enviado"})


CODE_PASSWORD_TOKEN_OK = 1  # Usuário tem um Password Token válido
CODE_PASSWORD_TOKEN_EXPIRED = 2  # Email seja agendado com um novo Password Token


@authentication_classes([])
@permission_classes([])
class ResetPassword(APIView):
    @swagger_auto_schema(
        query_serializer=serializers.ResetPasswordParamsSerializer,
        responses={200: serializers.ResetPasswordParamsForDocs},
    )
    def post(self, request):
        try:
            request_user_email = request.GET.get("email")
            Password.send_email_reset_password(request_user_email)
            response = EndpointsUtils.create_message_endpoint_response(
                status=EndpointsUtils.status_success,
                message="O email foi enviado para o usuário com link de redefinição de senha",
            )

            return Response(response, status.HTTP_200_OK)
        except Exception as error:
            response = EndpointsUtils.create_message_endpoint_response(
                status=EndpointsUtils.status_error, message=str(error)
            )

            return Response(response, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            request_token = request.GET.get("token")
            user, code_token = UserToken.get_user_by_token_and_set_invalid_tried(request_token)

            response = {
                "status": EndpointsUtils.status_success,
                "code": code_token,
                "message": "Token válido" if code_token == CODE_PASSWORD_TOKEN_OK else "Novo email será enviado",
                "email": user.email,
            }

            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([])
@permission_classes([])
class ConfirmResetPassword(APIView):
    @swagger_auto_schema(
        request_body=serializers.ConfirmPasswordBodySerializer, responses={200: serializers.ResetPasswordParamsForDocs}
    )
    def post(self, request):
        try:
            request_user_new_password = request.data["user_new_password"]
            request_user_reset_password_token = request.data["user_token"]
            Password.change_user_password(request_user_new_password, request_user_reset_password_token)
            response = EndpointsUtils.create_message_endpoint_response(
                status=EndpointsUtils.status_success, message="User password has been changed"
            )

            return Response(response, status.HTTP_200_OK)
        except Exception as error:
            response = EndpointsUtils.create_message_endpoint_response(
                status=EndpointsUtils.status_error, message=str(error)
            )

            return Response(response, status.HTTP_400_BAD_REQUEST)
