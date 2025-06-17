import logging
import os

from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from contracts.models import Contract, EnergyBill
from universities.models import ConsumerUnit
from users.requests_permissions import RequestsPermissions
from utils.mixins.cache_mixin import CacheModelMixin
from utils.subgroup_util import Subgroup

from . import serializers, services


class ContractViewSet(CacheModelMixin, ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = serializers.ContractSerializer
    cache_key_prefix = "contract_viewset"
    cache_timeout = 3600 * 6

    def create(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions
        body_consumer_unit_id = request.data["consumer_unit"]

        try:
            consumer_unit = ConsumerUnit.objects.get(id=body_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({"error": "consumer unit does not exist"}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        self.delete_view_cache()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.university_user_permissions
        contract = self.get_object()
        university_id = contract.consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        self.delete_view_cache()
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(query_serializer=serializers.ContractListParamsSerializer)
    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.default_users_permissions
        params_serializer = serializers.ContractListParamsSerializer(data=request.GET)

        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_consumer_unit_id = request.GET.get("consumer_unit_id")

        try:
            consumer_unit = ConsumerUnit.objects.get(id=request_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({"error": "consumer unit does not exist"}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        queryset = Contract.objects.filter(consumer_unit=consumer_unit.id)
        serializer = serializers.ContractSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data, status.HTTP_200_OK)

    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    def retrieve(self, request, pk=None):
        user_types_with_permission = RequestsPermissions.default_users_permissions
        contract = self.get_object()

        university_id = contract.consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(contract)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: serializers.ListSubgroupsSerializerForDocs(many=True)})
    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    @action(detail=False, methods=["get"], url_path="list-subgroups")
    def list_subgroups(self, request: Request, pk=None):
        try:
            subgroups = {"subgroups": Subgroup.get_all_subgroups()}
        except Exception as error:
            return Response({"list subgroups error": f"{error}"}, status.HTTP_400_BAD_REQUEST)

        return JsonResponse(subgroups, safe=False)

    @swagger_auto_schema(
        query_serializer=serializers.ContractListParamsSerializer, responses={200: serializers.ContractListSerializer}
    )
    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    @action(detail=False, methods=["get"], url_path="get-current-contract-of-consumer-unit")
    def get_current_contract_of_consumer_unit(self, request: Request, pk=None):
        user_types_with_permission = RequestsPermissions.university_user_permissions

        params_serializer = serializers.ContractListParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_consumer_unit_id = request.GET.get("consumer_unit_id")

        try:
            consumer_unit = ConsumerUnit.objects.get(id=request_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({"error": "consumer unit does not exist"}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        contract = consumer_unit.current_contract

        serializer = serializers.ContractListSerializer(contract, many=False, context={"request": request})
        return Response(serializer.data, status.HTTP_200_OK)


class EnergyBillViewSet(CacheModelMixin, ModelViewSet):
    queryset = EnergyBill.objects.all()
    serializer_class = serializers.EnergyBillSerializer
    cache_key_prefix = "energybill_viewset"
    cache_timeout = 3600 * 168  # 3600 segundos * 24  = 1 dia (dados nao mudam com frequência)

    def retrieve(self, request, pk=None):
        energy_bill = self.get_object()
        consumer_unit = energy_bill.consumer_unit

        try:
            RequestsPermissions.check_request_permissions(
                request.user, RequestsPermissions.default_users_permissions, consumer_unit.university.id
            )
        except Exception as error:
            return Response({"detail": f"{error}"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(energy_bill)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        energy_bill = self.get_object()
        consumer_unit = energy_bill.consumer_unit
        contract = energy_bill.contract

        try:
            RequestsPermissions.check_request_permissions(
                request.user, RequestsPermissions.default_users_permissions, consumer_unit.university.id
            )
            RequestsPermissions.check_request_permissions(
                request.user, RequestsPermissions.default_users_permissions, contract.consumer_unit.university.id
            )
        except Exception as error:
            return Response({"detail": f"{error}"}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        consumer_unit_id = request.data.get("consumer_unit")
        contract_id = request.data.get("contract")

        try:
            # Verifica se a unidade consumidora e o contrato existem
            try:
                consumer_unit = ConsumerUnit.objects.get(id=consumer_unit_id)
                contract = Contract.objects.get(id=contract_id)
            except ObjectDoesNotExist:
                return Response(
                    {"error": "Consumer unit or contract does not exist"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Verifica permissões
            try:
                RequestsPermissions.check_request_permissions(
                    request.user, RequestsPermissions.default_users_permissions, consumer_unit.university.id
                )
                RequestsPermissions.check_request_permissions(
                    request.user, RequestsPermissions.default_users_permissions, contract.consumer_unit.university.id
                )
            except Exception as error:
                return Response({"detail": str(error)}, status=status.HTTP_403_FORBIDDEN)

            # Tenta criar a fatura
            response = super().create(request, *args, **kwargs)
            return response

        except Exception as error:
            # Todas as outras exceções são tratadas como erros de validação
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        energy_bill = self.get_object()
        consumer_unit = energy_bill.consumer_unit
        contract = energy_bill.contract

        try:
            RequestsPermissions.check_request_permissions(
                request.user, RequestsPermissions.default_users_permissions, consumer_unit.university.id
            )
            RequestsPermissions.check_request_permissions(
                request.user, RequestsPermissions.default_users_permissions, contract.consumer_unit.university.id
            )
        except Exception as error:
            return Response({"detail": f"{error}"}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: serializers.EnergyBillListSerializerForDocs(many=True)},
        query_serializer=serializers.EnergyBillListParamsSerializer,
    )
    @method_decorator(cache_page(cache_timeout, key_prefix=cache_key_prefix))
    def list(self, request: Request, *args, **kwargs):
        user_types_with_permission = RequestsPermissions.default_users_permissions

        params_serializer = serializers.EnergyBillListParamsSerializer(data=request.GET)
        if not params_serializer.is_valid():
            return Response(params_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        request_consumer_unit_id = request.GET.get("consumer_unit_id")

        try:
            consumer_unit = ConsumerUnit.objects.get(id=request_consumer_unit_id)
        except ObjectDoesNotExist:
            return Response({"error": "consumer unit does not exist"}, status.HTTP_400_BAD_REQUEST)

        university_id = consumer_unit.university.id

        try:
            RequestsPermissions.check_request_permissions(request.user, user_types_with_permission, university_id)
        except Exception as error:
            return Response({"detail": f"{error}"}, status.HTTP_401_UNAUTHORIZED)

        energy_bills = consumer_unit.get_all_energy_bills()

        return Response(energy_bills)

    @action(detail=False, methods=["post"], url_path="multiple_create")
    def multiple_create(self, request, *args, **kwargs):
        consumer_unit_id = request.data.get("consumer_unit")
        contract_id = request.data.get("contract")
        energy_bills_data = request.data.get("energy_bills", [])
        response_data = []
        errors = []

        def round_value(value):
            if isinstance(value, int | float | Decimal):
                return str(Decimal(value).quantize(Decimal("1.00"), rounding=ROUND_HALF_UP))
            return value

        for bill_data in energy_bills_data:
            date_str = bill_data.get("date")

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                errors.append({"error": "Invalid date format", "data": bill_data})
                continue

            if EnergyBill.check_energy_bill_month_year(consumer_unit_id, date):
                errors.append(
                    {
                        "error": "There is already an energy bill this month and year for this consumer unit",
                        "data": bill_data,
                    }
                )
                continue

            if not EnergyBill.check_energy_bill_covered_by_contract(consumer_unit_id, date):
                errors.append({"error": "No contract covers the date of this energy bill", "data": bill_data})
                continue

            bill_data["consumer_unit"] = consumer_unit_id
            bill_data["contract"] = contract_id

            bill_data = {key: round_value(value) for key, value in bill_data.items()}

            serializer = self.get_serializer(data=bill_data)
            if not serializer.is_valid():
                errors.append({"error": "Validation error", "data": bill_data, "details": serializer.errors})

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        for bill_data in energy_bills_data:
            bill_data["consumer_unit"] = consumer_unit_id
            bill_data["contract"] = contract_id

            bill_data = {key: round_value(value) for key, value in bill_data.items()}

            serializer = self.get_serializer(data=bill_data)
            if serializer.is_valid():
                serializer.save()
                response_data.append(serializer.data)

        self.delete_related_view_cache(
            additional_viewsets=[
                "contracts.views.EnergyBillViewSet",
                "contracts.views.ContractViewSet",
                "universities.views.ConsumerUnitViewSet",
            ]
        )
        return Response({"created": response_data}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(method="post")
    @action(detail=False, methods=["post"], url_path="upload")
    def upload_csv(self, request, *args, **kwargs):
        logger = logging.getLogger("uc_sheet")
        energy_bill_data = []
        serializer = serializers.CSVFileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        consumer_unit_id = serializer.validated_data["consumer_unit_id"]
        logger.info(f"Consumer unit with id: {consumer_unit_id} is uploading a file")
        energy_bill_data = services.ContractServices().get_file_errors(
            serializer.validated_data["file"], consumer_unit_id
        )
        return Response({"data": energy_bill_data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="download-csv-model")
    def download_csv_model(self, request):
        file_path = os.path.join(settings.BASE_DIR, "docs", "modelo_importar_tarifas.csv")

        if os.path.exists(file_path):
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path))
        else:
            return Response("Document does not exist", status=400)

    @action(detail=False, methods=["get"], url_path="download-xlsx-model")
    def download_xlsx_model(self, request):
        file_path = os.path.join(settings.BASE_DIR, "docs", "modelo_importar_tarifas.xlsx")

        if os.path.exists(file_path):
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path))
        else:
            return Response("Document does not exist", status=400)

    @action(detail=False, methods=["get"], url_path="plot-graph")
    def plot_graph(self, request):
        consumer_unit_id = request.GET.get("consumer_unit_id")

        if not consumer_unit_id:
            return Response({"error": "consumer_unit_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        consumer_unit = ConsumerUnit.objects.get(id=consumer_unit_id)
        energy_bills = EnergyBill.objects.filter(
            consumer_unit=consumer_unit_id,
            date__gte=datetime.now().date() - timedelta(days=365),
        ).order_by("date")

        graph_data = {
            "energy_bills": energy_bills,
            "contract_data": consumer_unit.current_contract,
        }

        serializer = serializers.EnergyBillGraphSerializer(graph_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
