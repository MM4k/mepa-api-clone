import os
import re

from django.conf import settings
from django.db import IntegrityError
from django.http import FileResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from universities.models import ConsumerUnit
from users.requests_permissions import RequestsPermissions
from utils.endpoints_util import EndpointsUtils
from utils.mixins.cache_mixin import CacheModelMixin
from utils.tariff_util import response_tariffs_of_distributor

from .models import Distributor, Tariff
from .serializers import (
    BlueAndGreenTariffsSerializer,
    ConsumerUnitsSeparatedBySubgroupSerializerForDocs,
    DistributorListParamsSerializer,
    DistributorSerializer,
    GetTariffsOfDistributorForDocs,
    GetTariffsOfDistributorParamsSerializer,
    TariffSerializer,
)


class DistributorViewSet(CacheModelMixin, ModelViewSet):
    queryset = Distributor.objects.all()
    serializer_class = DistributorSerializer
    cache_key_prefix = "distributor_viewset"
    cache_timeout = 3600 * 24

    def destroy(self, request, *args, **kwargs):
        distributor: Distributor = self.get_object()
        user_types_with_permission = RequestsPermissions.default_users_permissions

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, distributor.university.id
            )
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        units = ConsumerUnit.objects.filter(university=distributor.university)

        blocking_units_ids = []
        for unit in units:
            current_contract = unit.current_contract

            if current_contract is not None:
                if current_contract.distributor.id == distributor.id:
                    blocking_units_ids.append(unit.id)

        if len(blocking_units_ids) != 0:
            return Response(
                {
                    "errors": ["There are active contracts associated to this distributor"],
                    "consumer_units_ids": blocking_units_ids,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        Distributor.objects.filter(pk=distributor.id).delete()
        self.delete_view_cache()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(query_serializer=DistributorListParamsSerializer)
    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        params_serializer = DistributorListParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_university_id = request.GET.get("university_id")
        request_only_pending = request.GET.get("only_pending")

        only_pending = (
            False
            if not request_only_pending
            else EndpointsUtils.convert_string_request_param_to_boolean(request_only_pending)
        )

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, request_university_id
            )
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        if only_pending:
            distributors = Distributor.get_distributors_pending(request_university_id)
        else:
            distributors = Distributor.objects.filter(university_id=request_university_id)

        ser = distributors.order_by(("name").lower())
        ser = DistributorSerializer(distributors, many=True, context={"request": request})
        return Response(ser.data, status.HTTP_200_OK)

    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    def retrieve(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.university_user_permissions
        distributor = self.get_object()

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, distributor.university.id
            )
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(distributor)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: ConsumerUnitsSeparatedBySubgroupSerializerForDocs()})
    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    @action(detail=True, methods=["get"], url_path="consumer-units-by-subgroup")
    def consumer_units_separated_by_subgroup(self, request: Request, pk=None):
        user_types_with_permission = RequestsPermissions.university_user_permissions
        distributor: Distributor = self.get_object()

        try:
            RequestsPermissions.check_request_permissions(
                request.user, user_types_with_permission, distributor.university.id
            )
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        consumer_units = distributor.get_consumer_units_separated_by_subgroup()
        return Response(consumer_units, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: GetTariffsOfDistributorForDocs()}, query_serializer=GetTariffsOfDistributorParamsSerializer
    )
    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    @action(detail=True, methods=["get"], url_path="get-tariffs")
    def get_blue_and_green_tariffs(self, request: Request, pk=None):
        user_types_with_permission = RequestsPermissions.default_users_permissions
        distributor: Distributor = self.get_object()

        params_serializer = GetTariffsOfDistributorParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        try:
            university_id = distributor.university.id

            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        request_subgroup = request.GET.get("subgroup")
        blue_tariff, green_tariff = distributor.get_tariffs_by_subgroups(request_subgroup)

        response = response_tariffs_of_distributor(
            blue_tariff.start_date if blue_tariff else None,
            blue_tariff.end_date if blue_tariff else None,
            blue_tariff.pending if blue_tariff else True,
            blue_tariff,
            green_tariff,
        )
        return Response(response, status.HTTP_200_OK)


class TariffViewSet(CacheModelMixin, ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer
    cache_key_prefix = "tariff_viewset"
    cache_timeout = 3600 * 24

    @swagger_auto_schema(request_body=BlueAndGreenTariffsSerializer)
    def create(self, request: Request, *args, **kwargs):
        ser = BlueAndGreenTariffsSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        start_date = data["start_date"]
        end_date = data["end_date"]
        distributor = data["distributor"]
        subgroup = data["subgroup"]
        try:
            Tariff.objects.bulk_create(
                [
                    Tariff(
                        **data["blue"],
                        subgroup=subgroup,
                        flag=Tariff.BLUE,
                        start_date=start_date,
                        end_date=end_date,
                        distributor=distributor,
                    ),
                    Tariff(
                        **data["green"],
                        subgroup=subgroup,
                        flag=Tariff.GREEN,
                        start_date=start_date,
                        end_date=end_date,
                        distributor=distributor,
                    ),
                ]
            )
        except IntegrityError as error:
            return self._handle_integrity_error(error)
        except Exception as e:
            raise e

        self.delete_view_cache()
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def _handle_integrity_error(self, error: IntegrityError):
        error_message = str(error)

        if "UNIQUE constraint failed:" in error_message:
            formatted_error = "There is already a tariff with given (subgroup, distributor, flag)=-"
            return Response({"errors": [formatted_error]}, status=status.HTTP_403_FORBIDDEN)
        elif "duplicate key value violates unique constraint" in error_message:
            duplicate_key = re.search(r"\)=(\(.*\))", error_message).groups(0)[0]
            formatted_error = f"There is already a tariff with given (subgroup, distributor, flag)={duplicate_key}"
            return Response({"errors": [formatted_error]}, status=status.HTTP_403_FORBIDDEN)
        else:
            raise error

    @swagger_auto_schema(request_body=BlueAndGreenTariffsSerializer)
    def update(self, request: Request, pk=None):
        """Essa rota de fato foge um pouco do padrão REST: ```PUT /api/tariffs/id```.
        Nesse caso, `id` NÃO É USADO, de maneira que `id` pode ser setado para
        qualquer coisa. Ainda assim, é possível identificar as tarifas pelo
        _subgrupo_ e _distribuidora_."""

        ser = BlueAndGreenTariffsSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        data = ser.validated_data
        tariffs = Tariff.objects.filter(subgroup=data["subgroup"], distributor=data["distributor"])
        if 0 == tariffs.count():
            return Response(
                {
                    "errors": [
                        f"Could not find tariffs with "
                        f"subgroup={data['subgroup']} and distributor_id={data['distributor'].id}"
                    ]
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        assert 2 == tariffs.count()

        start_date = data["start_date"]
        end_date = data["end_date"]

        for tariff in tariffs.filter(flag=Tariff.BLUE):
            for key, value in data["blue"].items():
                setattr(tariff, key, value)
            tariff.start_date = start_date
            tariff.end_date = end_date
            tariff.save()

        for tariff in tariffs.filter(flag=Tariff.GREEN):
            for key, value in data["green"].items():
                setattr(tariff, key, value)
            tariff.start_date = start_date
            tariff.end_date = end_date
            tariff.save()

        blue_tariff = Tariff.objects.filter(
            subgroup=data["subgroup"],
            distributor=data["distributor"],
            flag=Tariff.BLUE,
        ).first()

        green_tariff = Tariff.objects.filter(
            subgroup=data["subgroup"],
            distributor=data["distributor"],
            flag=Tariff.GREEN,
        ).first()

        ser = BlueAndGreenTariffsSerializer(
            {
                "start_date": start_date,
                "end_date": end_date,
                "distributor": data["distributor"],
                "subgroup": data["subgroup"],
                "blue": blue_tariff,
                "green": green_tariff,
            }
        )

        self.delete_view_cache()
        return Response(ser.data)


class DownloadPDFViewSet(ViewSet):
    def list(self, request):
        file_path = os.path.join(settings.BASE_DIR, "docs", "Pegar_tarifas_da_distribuidora_2023.pdf")

        if os.path.exists(file_path):
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path))
        else:
            return Response("Document does not exist", status=400)
