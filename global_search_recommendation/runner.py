from abc import ABC

from django.conf import settings
from sko.PSO import PSO

from global_search_recommendation.domain import Domain
from global_search_recommendation.recommendation import Recommendation
from tariffs.models import Tariff


class Runner(ABC):
    def __init__(self, domain: Domain) -> None:
        self.domain = domain
        self.history = domain.consumption_history
        self.p_lbound = max(
            self.history["peak_measured_demand_in_kw"].min(),
            settings.NEW_RESOLUTION_MINIMUM_DEMAND,
        )
        self.o_lbound = max(
            self.history["off_peak_measured_demand_in_kw"].min(),
            settings.NEW_RESOLUTION_MINIMUM_DEMAND,
        )
        self.p_ubound = max(self.history["peak_measured_demand_in_kw"].max(), self.p_lbound + 1)
        self.o_ubound = max(self.history["off_peak_measured_demand_in_kw"].max(), self.o_lbound + 1)
        self.g_lb = min(self.p_lbound, self.o_lbound)
        self.g_ub = max(self.p_ubound, self.o_ubound)

    def _check_bounds(self, lb: 0.0, up: 0.0):
        return up >= lb

    @classmethod
    def calculate(cls): ...


class PSORunner(Runner):
    def calculate(self):
        skip_green = self.domain.current_contract.subgroup in ["A2", "A3"]

        if self._check_bounds(lb=self.p_lbound, up=self.p_ubound) and self._check_bounds(
            lb=self.o_lbound, up=self.o_ubound
        ):
            blue = PSO(
                func=self.domain.blue_objective_func,
                n_dim=2,
                pop=40,
                max_iter=100,
                w=0.8,
                c1=0.6,
                c2=0.6,
                lb=[self.p_lbound, self.o_lbound],
                ub=[self.p_ubound, self.o_ubound],
            )
            blue.run()
        else:
            raise Exception("limites inválidos para computação da recomendação na modalidade azul")

        if self._check_bounds(lb=self.g_lb, up=self.g_ub):
            if not skip_green:
                green = PSO(
                    func=self.domain.green_objective_func,
                    n_dim=1,
                    pop=40,
                    max_iter=100,
                    w=0.8,
                    c1=0.6,
                    c2=0.6,
                    lb=self.g_lb,
                    ub=self.g_ub,
                )
                green.run()
        else:
            raise Exception("limites inválidos para computação da recomendação na modalidade verde")

        if not skip_green and green.gbest_y < blue.gbest_y:
            return Recommendation(
                Tariff.GREEN,
                (0, round(green.gbest_x[0], 2)),
                self.domain,
            )
        else:
            return Recommendation(
                Tariff.BLUE,
                (round(blue.gbest_x[0], 2), round(blue.gbest_x[1], 2)),
                self.domain,
            )
