from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer, ModelSerializer, Serializer

from tariffs.models import Tariff
from universities.models import University
from utils.cnpj_validator_util import CnpjValidator

from .models import Distributor


class BlueTariffSerializer(ModelSerializer):
    peak_tusd_in_reais_per_kw = serializers.FloatField(max_value=9999.99)
    peak_tusd_in_reais_per_mwh = serializers.FloatField(max_value=9999.99)
    peak_te_in_reais_per_mwh = serializers.FloatField(max_value=9999.99)
    off_peak_tusd_in_reais_per_kw = serializers.FloatField(max_value=9999.99)
    off_peak_tusd_in_reais_per_mwh = serializers.FloatField(max_value=9999.99)
    off_peak_te_in_reais_per_mwh = serializers.FloatField(max_value=9999.99)

    class Meta:
        model = Tariff
        fields = [
            "peak_tusd_in_reais_per_kw",
            "peak_tusd_in_reais_per_mwh",
            "peak_te_in_reais_per_mwh",
            "off_peak_tusd_in_reais_per_kw",
            "off_peak_tusd_in_reais_per_mwh",
            "off_peak_te_in_reais_per_mwh",
        ]


class GreenTariffSerializer(ModelSerializer):
    peak_tusd_in_reais_per_mwh = serializers.FloatField(max_value=9999.99, allow_null=True, required=False)
    peak_te_in_reais_per_mwh = serializers.FloatField(max_value=9999.99, allow_null=True, required=False)
    off_peak_tusd_in_reais_per_mwh = serializers.FloatField(max_value=9999.99, allow_null=True, required=False)
    off_peak_te_in_reais_per_mwh = serializers.FloatField(max_value=9999.99, allow_null=True, required=False)
    na_tusd_in_reais_per_kw = serializers.FloatField(max_value=9999.99, allow_null=True, required=False)

    class Meta:
        model = Tariff
        fields = [
            "peak_tusd_in_reais_per_mwh",
            "peak_te_in_reais_per_mwh",
            "off_peak_tusd_in_reais_per_mwh",
            "off_peak_te_in_reais_per_mwh",
            "na_tusd_in_reais_per_kw",
        ]


class BlueAndGreenTariffsSerializer(Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    subgroup = serializers.ChoiceField(allow_blank=False, choices=Tariff.subgroups)
    distributor = serializers.PrimaryKeyRelatedField(queryset=Distributor.objects.all())
    pending = serializers.BooleanField(read_only=True)
    blue = BlueTariffSerializer()
    green = GreenTariffSerializer()

    def validate(self, data):
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError("Start date must be before end date")
        return data

    class Meta:
        fields = "__all__"


class TariffSerializer(ModelSerializer):
    pending = serializers.BooleanField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Tariff


class DistributorSerializer(HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())
    # tariffs = TariffSerializer(many=True, read_only=True)
    # consumer_units = serializers.IntegerField(read_only=True)
    consumer_units_count = serializers.IntegerField(read_only=True)
    pending_tariffs_count = serializers.IntegerField(read_only=True)
    is_pending = serializers.BooleanField(read_only=True)

    class Meta:
        model = Distributor
        fields = "__all__"

    def validate_cnpj(self, cnpj: str):
        try:
            CnpjValidator.validate(cnpj)
        except Exception as e:
            raise serializers.ValidationError(str(e.args))
        return cnpj


class DistributorSerializerForDocs(DistributorSerializer):
    """Esse serializer é usado apenas para documentação no Swagger"""

    tariffs = BlueAndGreenTariffsSerializer(many=True)


class _ConsumerUnitSerializerForDocs(Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class _SubgroupSerializerForDocs(Serializer):
    sub_group = serializers.CharField(read_only=True)
    pending = serializers.BooleanField()
    consumer_units = _ConsumerUnitSerializerForDocs(many=True)


class ConsumerUnitsSeparatedBySubgroupSerializerForDocs(Serializer):
    sub_group = _SubgroupSerializerForDocs(many=True, read_only=True)


class DistributorListParamsSerializer(Serializer):
    only_pending = serializers.BooleanField()
    university_id = serializers.IntegerField()


class GetTariffsOfDistributorParamsSerializer(Serializer):
    subgroup = serializers.CharField()


class GetTariffsOfDistributorForDocs(Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    blue = BlueTariffSerializer()
    green = GreenTariffSerializer()
