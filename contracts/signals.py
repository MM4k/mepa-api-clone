from django.db.models.signals import post_save
from django.dispatch import receiver

from contracts.models import Contract, EnergyBill
from recommendation.models import Recommendation


@receiver(post_save, sender=Contract)
def trigger_contracts(sender, instance, created, **kwargs):
    consumer_unit = instance.consumer_unit
    try:
        recommendation_instance = Recommendation.objects.get(consumer_unit=consumer_unit.id)
        recommendation_instance.isValid = False
        recommendation_instance.save()
    except Recommendation.DoesNotExist:
        # print(f"Nenhuma recomendação encontrada para o consumidor: {consumer_unit.id}", flush=True)
        pass


@receiver(post_save, sender=EnergyBill)
def trigger_bills(sender, instance, created, **kwargs):
    consumer_unit = instance.consumer_unit

    try:
        # Tenta obter a instância de Recommendation
        recommendation_instance = Recommendation.objects.get(consumer_unit=consumer_unit.id)

        # Verifica se a lista de datas não está vazia
        if recommendation_instance.dates:
            start_date_calculated = min(recommendation_instance.dates)
            end_date_calculated = max(recommendation_instance.dates)
            in_date_range = start_date_calculated <= instance.date <= end_date_calculated
            in_tariff_range = (
                recommendation_instance.tariffStartDate <= instance.date <= recommendation_instance.tariffEndDate
            )
            after_tariff_end = instance.date >= recommendation_instance.tariffEndDate
            after_end_date = instance.date >= end_date_calculated

            if in_date_range or in_tariff_range or after_tariff_end or after_end_date:
                try:
                    recommendation_instance = Recommendation.objects.get(consumer_unit=consumer_unit.id)
                    recommendation_instance.isValid = False
                    recommendation_instance.save()
                except Recommendation.DoesNotExist:
                    # print(f"Nenhuma recomendação encontrada para o consumidor: {consumer_unit.id}", flush=True)
                    pass
            else:
                print("A data da fatura NÃO está no intervalo analisado", flush=True)
        else:
            print("A lista de datas na recomendação está vazia.", flush=True)

    except Recommendation.DoesNotExist:
        print(f"Nenhuma recomendação encontrada para a unidade consumidora: {consumer_unit.id}", flush=True)
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}", flush=True)
