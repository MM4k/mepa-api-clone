from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from recommendation.recommendation_utils import process_recommendation, save_recommendation
from universities.models import ConsumerUnit

from .models import Recommendation


class RecommendationViewSet(ViewSet):
    http_method_names = ["get"]

    def retrieve(self, request: Request, pk=None):
        """Recomendação via percentis. Deve ser fornecido o ID da Unidade Consumidora.

        `plotRecommendedDemands`: se a tarifa recomendada é VERDE, os campos
        `plotRecommendedDemands.offPeakDemandInKw` e
        `plotRecommendedDemands.peakDemandInKw`
        possuem o mesmo valor. Você pode plotar os dois ou plotar apenas um
        desses campos como demanda única.

        `table_current_vs_recommended_contract.absolute_difference = current - recommended`
        """

        consumer_unit_id = pk

        consumer_unit_instance = ConsumerUnit.objects.get(id=consumer_unit_id)
        try:
            # Tenta obter a recomendação existente
            recommendation = Recommendation.objects.filter(consumer_unit_id=consumer_unit_id).first()

            if recommendation is None or not recommendation.isValid:
                # Processa a nova recomendação
                pr = process_recommendation(consumer_unit_id)
                recommendation_instance, created = save_recommendation(consumer_unit_instance, *pr)
                recommendation = Recommendation.objects.get(consumer_unit_id=consumer_unit_id)

            # Se a recomendação é válida, retorna os dados
            data = recommendation.to_dict()
            return JsonResponse(data, safe=False)

        except ObjectDoesNotExist:
            print("Unidade de consumo não encontrada.", flush=True)
            return JsonResponse({"error": "Unidade de consumo não encontrada."}, status=404)
        except Exception as e:
            print(f"Ocorreu um erro: {e}", flush=True)
            return JsonResponse({"error": "Ocorreu um erro inesperado."}, status=500)
