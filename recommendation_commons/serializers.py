from rest_framework import serializers
from rest_framework.serializers import Serializer


class RecommendationSettingsSerializerForDocs(Serializer):
    MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION = serializers.IntegerField()
    IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION = serializers.IntegerField()
