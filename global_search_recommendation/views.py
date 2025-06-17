from pandas import DataFrame
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from global_search_recommendation.domain import Domain
from global_search_recommendation.runner import PSORunner
from recommendation_commons.helpers import fill_history_with_pending_dates
from recommendation_commons.response import build_response


class GlobalSearchRecommendationViewSet(ViewSet):
    http_method_names = ["get"]

    def retrieve(self, request: Request, pk=None):
        """Recomendação via busca global. Deve ser fornecido o ID da Unidade Consumidora."""

        domain = Domain(pk)
        domain_mount_result = domain.mount()

        if domain_mount_result:
            if len(domain.errors) > 0:
                fill_history_with_pending_dates(domain.consumption_history, domain.pending_bills_dates)
                return build_response(
                    None,
                    DataFrame(),
                    domain.consumption_history,
                    domain.current_contract,
                    domain.consumer_unit,
                    domain.blue,
                    domain.green,
                    domain.errors,
                    domain.warnings,
                    domain.consumption_history_length,
                )
            else:
                return Response(domain_mount_result)

        runner = PSORunner(domain)
        recomendation = runner.calculate()

        return recomendation.build_response()
