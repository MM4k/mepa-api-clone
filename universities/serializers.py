from django.db import transaction
from rest_framework import serializers

from contracts.models import Contract
from contracts.serializers import ContractSerializer
from universities.models import ConsumerUnit, University
from utils.cnpj_validator_util import CnpjValidator


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = [
            "id",
            "name",
            "acronym",
            "cnpj",
            "is_active",
            "created_on",
        ]

    def validate_cnpj(self, cnpj: str):
        try:
            CnpjValidator.validate(cnpj)
        except Exception as e:
            raise serializers.ValidationError(str(e.args))
        return cnpj


class ConsumerUnitSerializer(serializers.ModelSerializer):
    university = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ConsumerUnit
        fields = [
            "id",
            "name",
            "code",
            "is_active",
            "date",
            "is_current_energy_bill_filled",
            "pending_energy_bills_number",
            "university",
            "total_installed_power",
            "created_on",
        ]


class ConsumerUnitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerUnit
        fields = [
            "id",
            "name",
            "code",
            "university",
            "total_installed_power",
            "is_active",
            "created_on",
        ]
        read_only_fields = ["created_on"]


class ConsumerUnitWithContractSerializer(serializers.Serializer):
    consumer_unit = ConsumerUnitCreateSerializer()
    contract = ContractSerializer()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["consumer_unit"] = ConsumerUnitCreateSerializer(instance=self.instance)
            self.fields["contract"] = ContractSerializer(instance=self.instance.current_contract)

    @transaction.atomic
    def create(self, validated_data):
        consumer_unit_data = validated_data.pop("consumer_unit")
        contract_data = validated_data.pop("contract")
        consumer_unit = ConsumerUnit.objects.create(**consumer_unit_data)
        contract = Contract.objects.create(consumer_unit=consumer_unit, **contract_data)

        return {"consumer_unit": consumer_unit, "contract": contract}

    @transaction.atomic
    def update(self, instance, validated_data):
        contract_data = validated_data.pop("contract")
        consumer_unit_data = validated_data.pop("consumer_unit")

        consumer_unit = instance
        for attr, value in consumer_unit_data.items():
            setattr(consumer_unit, attr, value)
        consumer_unit.save()

        contract = consumer_unit.current_contract

        for attr, value in contract_data.items():
            if attr != "contract_id":
                setattr(contract, attr, value)
        contract.save()

        return {"consumer_unit": consumer_unit, "contract": contract}
