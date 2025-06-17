from datetime import date

from django.conf import settings

from utils.energy_bill_util import EnergyBillUtils


# Testa a geração de datas em um intervalo válido
def test_generate_dates_valid_range():
    start_date = date(2020, 1, 1)
    end_date = date(2020, 12, 31)
    result = EnergyBillUtils.generate_dates(start_date, end_date)
    assert len(result) == 1
    assert "2020" in result
    assert len(result["2020"]) == 12


# Testa a geração de datas em um intervalo inválido
def test_generate_dates_invalid_range():
    start_date = date(2021, 1, 1)
    end_date = date(2020, 12, 31)
    result = EnergyBillUtils.generate_dates(start_date, end_date)
    assert len(result) == 0


# Verifica se a data está na lista de recomendações
def test_is_date_be_on_recommendation_list_true():
    recommendation_dates = [{"month": 6, "year": 2021}, {"month": 7, "year": 2021}]
    search_date = {"month": 6, "year": 2021}
    result = EnergyBillUtils.is_date_be_on_recommendation_list(recommendation_dates, search_date)
    assert result is True


# Verifica se a data não está na lista de recomendações
def test_is_date_be_on_recommendation_list_false():
    recommendation_dates = [{"month": 6, "year": 2021}, {"month": 7, "year": 2021}]
    search_date = {"month": 8, "year": 2021}
    result = EnergyBillUtils.is_date_be_on_recommendation_list(recommendation_dates, search_date)
    assert result is False


# Testa a atualização da data e inserção na lista de contas de energia
def test_update_date_and_insert_energy_bill_on_list():
    energy_bills_list = []
    month = 6
    year = 2021
    updated_list, updated_month, updated_year = EnergyBillUtils.update_date_and_insert_energy_bill_on_list(
        energy_bills_list, month, year
    )

    assert len(updated_list) == 1
    assert updated_list[0]["month"] == 5  # Assume que o método decrementa o mês
    assert updated_list[0]["year"] == 2021
    assert updated_month == 5
    assert updated_year == 2021


# Testa a geração de datas recentes para recomendação
def test_generate_latest_dates_for_recommendation():
    result = EnergyBillUtils.generate_latest_dates_for_recommendation()
    assert len(result) == settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION  # Assume um número fixo de datas geradas


# Testa a geração de datas para um ano específico
def test_generate_dates_by_year():
    year = 2021
    result = EnergyBillUtils.generate_dates_by_year(year)
    assert (
        len(result) == settings.IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION
    )  # Assume um número fixo de datas geradas para o ano dado
