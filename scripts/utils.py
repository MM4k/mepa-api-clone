from datetime import date, timedelta
from random import randint, uniform

YEAR_LATER = date.today() + timedelta(days=2 * 365)

BLUE_TARIFF = {
    "peak_tusd_in_reais_per_kw": 29.84,
    "peak_tusd_in_reais_per_mwh": 127.2,
    "peak_te_in_reais_per_mwh": 620.43,
    "off_peak_tusd_in_reais_per_kw": 12.0,
    "off_peak_tusd_in_reais_per_mwh": 127.2,
    "off_peak_te_in_reais_per_mwh": 392.71,
    "power_generation_tusd_in_reais_per_kw": 10.00,
}

GREEN_TARIFF = {
    "peak_tusd_in_reais_per_mwh": 852.45,
    "peak_te_in_reais_per_mwh": 620.43,
    "off_peak_tusd_in_reais_per_mwh": 127.2,
    "off_peak_te_in_reais_per_mwh": 392.71,
    "na_tusd_in_reais_per_kw": 13.0,
    "power_generation_tusd_in_reais_per_kw": 10.00,
}

TABLE_BILLS = [
    ["2023-05-01", 10430.0, 15786.0, 0.0, 361.0, 0, "False"],
    ["2023-06-01", 10689.0, 18307.0, 0.0, 380.0, 0, "False"],
    ["2023-07-01", 11537.0, 17667.0, 0.0, 489.0, 0, "False"],
    ["2023-08-01", 12700.0, 16986.0, 0.0, 369.0, 0, "False"],
    ["2023-09-01", 12419.0, 17248.0, 0.0, 476.0, 0, "False"],
    ["2023-10-01", 11738.0, 17355.0, 0.0, 572.0, 0, "False"],
    ["2023-11-01", 13571.0, 14740.0, 0.0, 395.0, 0, "False"],
    ["2023-12-01", 12558.0, 14961.0, 0.0, 495.0, 0, "False"],
    ["2024-01-01", 11966.0, 13244.0, 0.0, 395.0, 0, "False"],
    ["2024-02-01", 11086.0, 12515.0, 0.0, 610.0, 0, "False"],
    ["2024-03-01", 12260.0, 16189.0, 0.0, 511.0, 0, "False"],
    ["2024-04-01", 12055.0, 14498.0, 0.0, 410.0, 0, "False"],
    ["2024-05-01", 11933.0, 15786.0, 0.0, 561.0, 0, "False"],
    ["2024-06-01", 10811.0, 17377.0, 0.0, 480.0, 0, "False"],
    ["2024-07-01", 13637.0, 16699.0, 0.0, 389.0, 0, "False"],
    ["2024-08-01", 14700.0, 17955.0, 0.0, 569.0, 0, "False"],
    ["2024-09-01", 15819.0, 18248.0, 0.0, 476.0, 0, "False"],
]

UNIVERSITY_TEMPLATES = [
    ("Universidade Federal de {}", "UF{}"),
    ("Universidade Estadual de {}", "UE{}"),
    ("Instituto Federal de {}", "IF{}"),
    ("Centro Universitário {}", "UNI{}"),
]

REGIONS = [
    ("Distrito Federal", "DF"),
    ("São Paulo", "SP"),
    ("Rio de Janeiro", "RJ"),
    ("Bahia", "BA"),
    ("Paraná", "PR"),
    ("Santa Catarina", "SC"),
    ("Goiás", "GO"),
    ("Pernambuco", "PE"),
    ("Ceará", "CE"),
    ("Amazonas", "AM"),
]

UC_TEMPLATES = [
    "Campus Universitário",
    "Centro de Tecnologia",
    "Instituto de Ciências",
    "Biblioteca Central",
    "Centro de Convivência",
    "Hospital Universitário",
    "Centro de Pesquisas",
    "Complexo Esportivo",
    "Residência Universitária",
    "Unidade de Ensino e Docência",
]

ENERGY_DISTRIBUTORS = [
    {"name": "ENERGISA SERGIPE DISTRIBUIDORA DE ENERGIA SA", "cnpj": "13017462000163"},
    {"name": "AMAZONAS ENERGIA SA", "cnpj": "02341467000120"},
    {"name": "CEMIG DISTRIBUICAO SA", "cnpj": "06981180000116"},
    {"name": "COMPANHIA DE ELETRICIDADE DO ESTADO DA BAHIA COELBA", "cnpj": "15139629000194"},
    {"name": "EQUATORIAL GOIAS DISTRIBUIDORA DE ENERGIA SA", "cnpj": "01543032000104"},
    {"name": "COPEL DISTRIBUICAO SA", "cnpj": "04368898000106"},
    {"name": "RGE SUL DISTRIBUIDORA DE ENERGIA SA", "cnpj": "02016440000162"},
    {"name": "ELETROPAULO METROPOLITANA ELETRICIDADE DE SAO PAULO SA", "cnpj": "61695227000193"},
    {"name": "AMPLA ENERGIA E SERVICOS SA", "cnpj": "33050071000158"},
    {"name": "EQUATORIAL PARA DISTRIBUIDORA DE ENERGIA SA", "cnpj": "04895728000180"},
]


def generate_cnpj():
    def calculate_digit(numbers: list) -> int:
        ma = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        mb = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        multipliers = ma if len(numbers) == 12 else mb

        soma = sum(a * b for a, b in zip(numbers, multipliers))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    numbers = [randint(0, 9) for _ in range(12)]
    numbers.append(calculate_digit(numbers))
    numbers.append(calculate_digit(numbers))
    return "".join(str(n) for n in numbers)


def get_data_university():
    for template, acronym_template in UNIVERSITY_TEMPLATES:
        for region, acronym in REGIONS:
            yield {
                "name": template.format(region),
                "acronym": acronym_template.format(acronym),
                "cnpj": generate_cnpj(),
            }


def add_random_variation(value, variation_percent=0.2):
    min_value = value * (1 - variation_percent)
    max_value = value * (1 + variation_percent)
    return round(uniform(min_value, max_value), 2)
