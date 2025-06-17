from datetime import date

from rest_framework import serializers

from contracts.models import Contract, EnergyBill
from contracts.validators import CsvFileValidator
from tariffs.models import Distributor
from universities.models import ConsumerUnit


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "consumer_unit",
            "distributor",
            "start_date",
            "end_date",
            "tariff_flag",
            "subgroup",
            "peak_contracted_demand_in_kw",
            "off_peak_contracted_demand_in_kw",
        ]
        read_only_fields = ["end_date"]
        extra_kwargs = {
            "consumer_unit": {"required": False},
            "start_date": {"required": True},
        }

    def validate(self, attrs):
        if "start_date" not in attrs:
            raise serializers.ValidationError({"start_date": "This field is required."})

        peak_contracted_demand_in_kw = attrs.get("peak_contracted_demand_in_kw")
        off_peak_contracted_demand_in_kw = attrs.get("off_peak_contracted_demand_in_kw")

        if peak_contracted_demand_in_kw < 30 or off_peak_contracted_demand_in_kw < 30:
            raise serializers.ValidationError("Um contrato não pode ter valores de demanda inferiores a 30kW")

        # Validação usando as choices do modelo
        tariff_flag = attrs.get("tariff_flag")
        subgroup = attrs.get("subgroup")

        for field in ["tariff_flag", "subgroup"]:
            choices = dict(getattr(Contract, f"{field}_choices"))
            if (value := locals()[field]) and value not in choices:
                raise serializers.ValidationError(
                    {field: f"Invalid value '{value}'. Allowed values are: {list(choices.keys())}"}
                )

        return attrs

    def validate_start_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("The start date cannot be in the future")
        return value


class ContractListSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    subgroup = serializers.CharField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    consumer_unit = serializers.PrimaryKeyRelatedField(queryset=ConsumerUnit.objects.all())
    distributor = serializers.PrimaryKeyRelatedField(queryset=Distributor.objects.all())
    distributor_name = serializers.CharField(source="get_distributor_name")
    university_name = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = fields = [
            "url",
            "id",
            "consumer_unit",
            "distributor",
            "distributor_name",
            "university_name",
            "start_date",
            "end_date",
            "tariff_flag",
            "subgroup",
            "peak_contracted_demand_in_kw",
            "off_peak_contracted_demand_in_kw",
        ]

    def get_university_name(self, obj):
        return obj.consumer_unit.university.name if obj.consumer_unit else None


class EnergyBillSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    contract = serializers.PrimaryKeyRelatedField(queryset=Contract.objects.all())
    consumer_unit = serializers.PrimaryKeyRelatedField(queryset=ConsumerUnit.objects.all())

    class Meta:
        model = EnergyBill
        fields = "__all__"


class ContractDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "peak_contracted_demand_in_kw",
            "off_peak_contracted_demand_in_kw",
        ]


class EnergyBillListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyBill
        fields = [
            "date",
            "is_atypical",
            "peak_consumption_in_kwh",
            "off_peak_consumption_in_kwh",
            "peak_measured_demand_in_kw",
            "off_peak_measured_demand_in_kw",
        ]


# invoice_in_reais = models.DecimalField(de


class EnergyBillGraphSerializer(serializers.Serializer):
    contract_data = ContractDemandSerializer(read_only=True)
    energy_bills = EnergyBillListSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        bills = repr.pop("energy_bills")
        consumption_history_plot = {
            "date": [bill["date"] for bill in bills],
            "peak_consumption_in_kwh": [bill["peak_consumption_in_kwh"] for bill in bills],
            "off_peak_consumption_in_kwh": [bill["off_peak_consumption_in_kwh"] for bill in bills],
            "peak_measured_demand_in_kw": [bill["peak_measured_demand_in_kw"] for bill in bills],
            "off_peak_measured_demand_in_kw": [bill["off_peak_measured_demand_in_kw"] for bill in bills],
        }
        repr["consumption_history_plot"] = consumption_history_plot
        return repr


class ContractListParamsSerializer(serializers.Serializer):
    consumer_unit_id = serializers.IntegerField()


class EnergyBillListParamsSerializer(serializers.Serializer):
    consumer_unit_id = serializers.IntegerField()


class SubgroupSerializerForDocs(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    min = serializers.CharField(read_only=True)
    max = serializers.CharField(read_only=True)


class ListSubgroupsSerializerForDocs(serializers.Serializer):
    subgroups = SubgroupSerializerForDocs(many=True, read_only=True)


class EnergyBillListObjectAttributesSerializerForDocs(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()
    invoice_in_reais = serializers.DecimalField(decimal_places=2, max_digits=10)
    is_atypical = serializers.BooleanField()
    peak_consumption_in_kwh = serializers.DecimalField(decimal_places=2, max_digits=9)
    off_peak_consumption_in_kwh = serializers.DecimalField(decimal_places=2, max_digits=9)
    off_peak_contracted_demand_in_kw = serializers.DecimalField(decimal_places=2, max_digits=10)
    peak_measured_demand_in_kw = serializers.DecimalField(decimal_places=2, max_digits=9)
    off_peak_measured_demand_in_kw = serializers.DecimalField(decimal_places=2, max_digits=9)
    energy_bill_file = serializers.FileField()


class EnergyBillListObjectSerializerForDocs(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    is_energy_bill_pending = serializers.BooleanField()
    energy_bill = EnergyBillListObjectAttributesSerializerForDocs()


class EnergyBillListSerializerForDocs(serializers.Serializer):
    year = EnergyBillListObjectSerializerForDocs(many=True, read_only=True)


class CSVFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    consumer_unit_id = serializers.IntegerField()

    def validate_file(self, file):
        validator = CsvFileValidator()
        return validator(file)
