from django.db.models.signals import post_save
from django.dispatch import receiver

from contracts.models import Contract
from recommendation.models import Recommendation
from tariffs.models import Tariff


@receiver(post_save, sender=Tariff)
def trigger_tariffs(sender, instance, created, **kwargs):
    distributor = instance.distributor
    subgroup = instance.subgroup
    contracts = Contract.objects.filter(distributor=distributor, subgroup=subgroup)

    impacted_consumer_units = contracts.values_list("consumer_unit", flat=True)

    for unit in impacted_consumer_units:
        try:
            recommendation_instance = Recommendation.objects.get(consumer_unit=unit)
            recommendation_instance.isValid = False
            recommendation_instance.save()
            # print(f"Recomendação inválida para o consumidor: {unit}", flush=True)
        except Recommendation.DoesNotExist:
            # print(f"Nenhuma recomendação encontrada para o consumidor: {unit}", flush=True)
            pass
