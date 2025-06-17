from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from universities.models import ConsumerUnit

from .models import UniversityUser
from .permissions import UniversityUserPermission
from .serializers import (
    FavoriteConsumerUnitActionSerializer,
    RetrieveUniversityUserSerializer,
    UniversityUserSerializer,
)


class UniversityUsersViewSet(ModelViewSet):
    queryset = UniversityUser.objects.all()
    serializer_class = UniversityUserSerializer
    permission_classes = [UniversityUserPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_admin:
            return UniversityUser.objects.all()
        university_user = UniversityUser.objects.get(id=user.id)
        if user.is_manager:
            return UniversityUser.objects.filter(university=university_user.university)
        return UniversityUser.objects.filter(id=user.id)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_staff or user.is_admin:
            serializer.save()
            return

        university_id = UniversityUser.objects.filter(id=user.id).values_list("university", flat=True).first()
        user_type = serializer.validated_data.get("type")
        allowed_types = [
            UniversityUser.Type.UNIVERSITY_ADMIN,
            UniversityUser.Type.UNIVERSITY_USER,
            UniversityUser.Type.UNIVERSITY_GUEST,
        ]
        if user.is_operational or user.is_guest:
            raise PermissionDenied("Common users cannot create accounts.")
        elif user_type not in allowed_types:
            raise PermissionDenied("Managers can only create 'university_admin' or 'university_user' accounts.")

        serializer.save(university_id=university_id)

    def perform_destroy(self, serializer):
        user = self.request.user
        if user.is_staff:
            serializer.delete()
        else:
            raise PermissionDenied("Only super_admin can delete an account.")

    def perform_update(self, serializer):
        user = self.request.user
        if user.is_staff or user.is_admin:
            serializer.save()
            return
        university_user = UniversityUser.objects.get(id=user.id)
        user_type = serializer.validated_data.get("type")
        if user.is_manager:
            if user_type == "super_user":
                raise PermissionDenied("Managers cannot change type to 'super_user'.")
            serializer.save(university=university_user.university)
        else:
            serializer.save(university=university_user.university, type=university_user.type)

    def get_serializer_class(self):
        if self.request.method == "retrieve":
            return RetrieveUniversityUserSerializer
        return UniversityUserSerializer

    @swagger_auto_schema(request_body=FavoriteConsumerUnitActionSerializer)
    @action(detail=True, methods=["post"], url_path="favorite-consumer-units")
    def add_or_remove_favorite_consumer_unit(self, request: Request, pk=None):
        params_serializer = FavoriteConsumerUnitActionSerializer(data=request.data)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user: UniversityUser = self.get_object()
        data = params_serializer.validated_data
        consumer_unit_id = data["consumer_unit_id"]
        action = data["action"]

        try:
            user.add_or_remove_favorite_consumer_unit(consumer_unit_id, action)
        except ConsumerUnit.DoesNotExist:
            return Response({"errors": ["Consumer unit not found"]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": e.args}, status=status.HTTP_403_FORBIDDEN)

        return Response(data, status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="change-user-password")
    def change_user_password(self, request: Request, pk=None):
        user = request.user
        data = request.data

        current_password = data.get("current_password")
        new_password = data.get("new_password")

        if not current_password or not new_password:
            return Response({"error": "Todos os campos são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UniversityUser.objects.get(id=user.id)
            user.change_user_password(current_password, new_password)
        except UniversityUser.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Senha alterada com sucesso"}, status=status.HTTP_200_OK)
