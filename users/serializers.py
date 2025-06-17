from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from universities.serializers import ConsumerUnitSerializer

from .models import University, UniversityUser


class UniversityUserSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())
    university_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UniversityUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "password",
            "email",
            "type",
            "created_on",
            "university",
            "university_name",
            "account_password_status",
            "have_reset_password_token_enable",
        ]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def get_university_name(self, obj):
        try:
            university_user = UniversityUser.objects.get(pk=obj.pk)
            return (
                f"{university_user.university.acronym} - {university_user.university.name}"
                if university_user.university
                else None
            )
        except UniversityUser.DoesNotExist:
            return None


class RetrieveUniversityUserSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())
    type = serializers.CharField(read_only=True)
    favorite_consumer_units = ConsumerUnitSerializer(read_only=True, many=True)

    class Meta:
        model = UniversityUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "password",
            "email",
            "type",
            "university",
            "favorite_consumer_units",
        ]
        extra_kwargs = {"password": {"write_only": True}}


class FavoriteConsumerUnitActionSerializer(Serializer):
    action = serializers.ChoiceField(allow_blank=False, choices=["remove", "add"])
    consumer_unit_id = serializers.IntegerField()


class ListUsersParamsSerializer(Serializer):
    university_id = serializers.IntegerField()


class ChangeUniversityUserTypeSerializer(Serializer):
    user_id = serializers.IntegerField()
    new_user_type = serializers.CharField()


class UniversityUserAuthenticatedSerializerForDocs(ModelSerializer):
    email = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())

    class Meta:
        model = UniversityUser
        fields = ["email", "first_name", "last_name", "type", "university"]


class AuthenticationTokenSerializerForDocs(Serializer):
    token = serializers.Field()
    user = UniversityUserAuthenticatedSerializerForDocs()


class AuthenticationGetTokenParamsSerializer(Serializer):
    token = serializers.ReadOnlyField()


class AuthenticationGetTokenSerializerForDocs(Serializer):
    is_valid_token = serializers.BooleanField()


## Authentications Endpoints


class ResetPasswordParamsSerializer(Serializer):
    email = serializers.CharField()


class ResetPasswordParamsForDocs(Serializer):
    status = serializers.CharField()
    message = serializers.CharField()


class ConfirmPasswordBodySerializer(Serializer):
    user_email = serializers.CharField()
    user_new_password = serializers.CharField()
    user_reset_password_token = serializers.CharField()
