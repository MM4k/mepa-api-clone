#!/usr/local/bin/python

from random import random
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from users.models import UniversityUser
from contracts.models import Contract
from universities.models import University, ConsumerUnit
from tariffs.models import Distributor, Tariff
from contracts.models import Contract, EnergyBill
from users.models import UniversityUser

TODAY = date.today()
YEAR_LATER = TODAY + timedelta(days=2*365)

##########################################################################
# Funções Auxiliares
##########################################################################

def create_bills_from_table(contract, uc, table):
    for row in table:
        EnergyBill.objects.create(contract=contract, consumer_unit=uc, \
            date=row[0],\
            peak_consumption_in_kwh=row[1],\
            off_peak_consumption_in_kwh=row[2],\
            peak_measured_demand_in_kw=row[3],\
            off_peak_measured_demand_in_kw=row[4],\
            invoice_in_reais=row[5],\
            is_atypical=(False if len(row) < 7 else row[6]))

def data_size(list):
    size = len(list)

    return size

def update_data(list, size):
    current_date = datetime.now().date()
    n_months = size - 1

    for i in range(size):
        new_date = current_date - relativedelta(months=n_months - i)
        list[i][0] = new_date.strftime('%Y-%m-%d')

    return list

##########################################################################

# Universidade

university = University.objects.create(
    name='Universidade Federal de Minas Gerais',
    acronym='UFMG',
    cnpj='17217985000104'
)

# Usuários

admin_university_user = UniversityUser.objects.create(
    university=university,
    type=UniversityUser.Type.UNIVERSITY_ADMIN,
    password='ufmg',
    email='admin@ufmg.br',
    first_name="João",
    last_name="da Silva",
    is_seed_user=True
)

university_user = UniversityUser.objects.create(
    university=university,
    type=UniversityUser.Type.UNIVERSITY_USER,
    password='ufmg',
    email='usuario@ufmg.br',
    first_name="José",
    last_name="Santos",
    is_seed_user=True
)

# Distribuidoras

distributor_cemig = Distributor.objects.create(
    name='CEMIG',
    cnpj='06981180000116',
    university=university,
)

distributor_dme = Distributor.objects.create(
    name='DME',
    cnpj='23664303000104',
    university=university,
)

distributor_elektro = Distributor.objects.create(
    name='Elektro',
    cnpj='02328280000197',
    university=university,
)


distributor_rge = Distributor.objects.create(
    name='RGE',
    cnpj='02016440000162',
    university=university,
)

distributor_ceee = Distributor.objects.create(
    name='CEEE',
    cnpj='08467115000100',
    university=university,
)

# Tarifas
blue = {
    "peak_tusd_in_reais_per_kw": 89.29,
    "peak_tusd_in_reais_per_mwh": 117.13,
    "peak_te_in_reais_per_mwh": 413.03,
    "off_peak_tusd_in_reais_per_kw": 31.53,
    "off_peak_tusd_in_reais_per_mwh": 117.13,
    "off_peak_te_in_reais_per_mwh": 260.02,
    "power_generation_tusd_in_reais_per_kw": 10.00
}
green = {
    "peak_tusd_in_reais_per_mwh": 2280.15,
    "peak_te_in_reais_per_mwh": 413.03,
    "off_peak_tusd_in_reais_per_mwh": 117.13,
    "off_peak_te_in_reais_per_mwh": 260.02,
    "na_tusd_in_reais_per_kw": 31.53,
    "power_generation_tusd_in_reais_per_kw": 10.00
}

a1_start_date = date(2023,6,17)
a1_end_date   = date(2024,5,12)
a3_start_date = date(2023,10,2)
a3_end_date   = date(2024,10,5)


Tariff.objects.bulk_create([
    Tariff(subgroup='A1', distributor=distributor_cemig, flag=Tariff.BLUE, **blue, start_date=a1_start_date, end_date=a1_end_date),
    Tariff(subgroup='A1', distributor=distributor_cemig, flag=Tariff.GREEN, **green, start_date=a1_start_date, end_date=a1_end_date),
    Tariff(subgroup='A3', distributor=distributor_cemig, flag=Tariff.BLUE, **blue, start_date=a3_start_date, end_date=a3_end_date),
    Tariff(subgroup='A3', distributor=distributor_cemig, flag=Tariff.GREEN, **green, start_date=a3_start_date, end_date=a3_end_date),
    Tariff(subgroup='A3a', distributor=distributor_cemig, flag=Tariff.BLUE, **blue, start_date=a3_start_date, end_date=a3_end_date),
    Tariff(subgroup='A3a', distributor=distributor_cemig, flag=Tariff.GREEN, **green, start_date=a3_start_date, end_date=a3_end_date),
    Tariff(subgroup='A4', distributor=distributor_cemig, flag=Tariff.BLUE, **blue, start_date=a1_start_date, end_date=a1_end_date),
    Tariff(subgroup='A4', distributor=distributor_cemig, flag=Tariff.GREEN, **green, start_date=a1_start_date, end_date=a1_end_date),
    Tariff(subgroup='AS', distributor=distributor_cemig, flag=Tariff.BLUE, **blue, start_date=a1_start_date, end_date=a1_end_date),
    Tariff(subgroup='AS', distributor=distributor_cemig, flag=Tariff.GREEN, **green, start_date=a1_start_date, end_date=a1_end_date),

])

Tariff.objects.bulk_create([
    Tariff(subgroup='A4', distributor=distributor_dme, flag=Tariff.BLUE, **blue, start_date=a1_start_date, end_date=a1_end_date),
    Tariff(subgroup='A4', distributor=distributor_dme, flag=Tariff.GREEN, **green, start_date=a1_start_date, end_date=a1_end_date),
])

Tariff.objects.bulk_create([
    Tariff(subgroup='A4', distributor=distributor_elektro, flag=Tariff.BLUE, **blue, start_date=a1_start_date, end_date=a1_end_date),
    Tariff(subgroup='A4', distributor=distributor_elektro, flag=Tariff.GREEN, **green, start_date=a1_start_date, end_date=a1_end_date),
])

# Unidades Consumidoras

uc_campus_centro = ConsumerUnit.objects.create(
    name='Campus Centro',
    code='1090000019',
    is_active=True,
    university=university,
)

contract2 = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_campus_centro,
    distributor=distributor_cemig,
    start_date=date(2023,1,1),
    subgroup="A3",
    peak_contracted_demand_in_kw=1000,
    off_peak_contracted_demand_in_kw=1680,
)

uc_campus_pampulha = ConsumerUnit.objects.create(
    name='Campus Pampulha',
    code='9006211',
    is_active=True,
    university=university,
)

contract_campus_pampulha = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_campus_pampulha,
    distributor=distributor_cemig,
    start_date=date(2023,2,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=150,
    off_peak_contracted_demand_in_kw=100,
)

uc_montes_claros = ConsumerUnit.objects.create(
    name='Montes Claros - Instituto de Ciências Agrárias',
    code='9004368',
    is_active=True,
    university=university,
)

contract_montes_claros = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_montes_claros,
    distributor=distributor_elektro,
    start_date=date(2022,1,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=350,
    off_peak_contracted_demand_in_kw=600,
)

uc_fazenda_modelo = ConsumerUnit.objects.create(
    name='Fazenda modelo',
    code='9001888',
    is_active=True,
    university=university,
)

contract_fazenda_modelo_0 = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_fazenda_modelo,
    distributor=distributor_ceee,
    start_date=date(2022,1,1),
    end_date=date(2023,12,31),
    subgroup="A4",
    peak_contracted_demand_in_kw=150,
    off_peak_contracted_demand_in_kw=150,
)

contract_fazenda_modelo = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_fazenda_modelo,
    distributor=distributor_cemig,
    start_date=date(2024,1,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=150,
    off_peak_contracted_demand_in_kw=150,
)

uc_fazenda_experimental = ConsumerUnit.objects.create(
    name='Fazenda experimental',
    code='9001889',
    is_active=False,
    university=university,
)

contract_fazenda_experimental = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_fazenda_experimental,
    distributor=distributor_cemig,
    start_date=date(2023,4,1),
    subgroup="A2",
    peak_contracted_demand_in_kw=300,
    off_peak_contracted_demand_in_kw=385,
)

uc_pampulha_ru_i = ConsumerUnit.objects.create(
    name='Pampulha - RU I',
    code='9001893',
    is_active=True,
    university=university,
)

contract_pampulha_ru_i = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_pampulha_ru_i,
    distributor=distributor_cemig,
    start_date=date(2022,10,1),
    subgroup="AS",
    peak_contracted_demand_in_kw=300,
    off_peak_contracted_demand_in_kw=385,
)

uc_pampulha_ru_ii = ConsumerUnit.objects.create(
    name='Pampulha - RU II',
    code='700081744',
    is_active=True,
    university=university,
)

contract_pampulha_ru_ii = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_pampulha_ru_ii,
    distributor=distributor_cemig,
    start_date=date(2022,12,1),
    subgroup="AS",
    peak_contracted_demand_in_kw=300,
    off_peak_contracted_demand_in_kw=385,
)

uc_pampulha_praca = ConsumerUnit.objects.create(
    name='Pampulha - Praça de serviços',
    code='9002456',
    is_active=True,
    university=university,
)

contract_pampulha_praca = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_pampulha_praca,
    distributor=distributor_cemig,
    start_date=date(2022,10,1),
    subgroup="AS",
    peak_contracted_demand_in_kw=250,
    off_peak_contracted_demand_in_kw=350,
)

uc_diamantina = ConsumerUnit.objects.create(
    name='Diamantina - Instituto casa da Glória',
    code='9050456',
    is_active=True,
    university=university,
)

contract_diamantina = Contract.objects.create(
    tariff_flag=Tariff.GREEN,
    consumer_unit=uc_diamantina,
    distributor=distributor_dme,
    start_date=date(2022,8,1),
    subgroup="A4",
    peak_contracted_demand_in_kw=300,
    off_peak_contracted_demand_in_kw=300,
)

uc_pampulha_teatro = ConsumerUnit.objects.create(
    name='Pampulha - Teatro',
    code='9342456',
    is_active=True,
    university=university,
)

contract_pampulha_teatro = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_pampulha_teatro,
    distributor=distributor_cemig,
    start_date=date(2023,10,1),
    subgroup="A3a",
    peak_contracted_demand_in_kw=250,
    off_peak_contracted_demand_in_kw=350,
)

uc_campus_tiradentes = ConsumerUnit.objects.create(
    name='Campus Tiradentes',
    code='9883556',
    is_active=True,
    university=university,
)

contract_campus_tiradentes = Contract.objects.create(
    tariff_flag=Tariff.BLUE,
    consumer_unit=uc_campus_tiradentes,
    distributor=distributor_cemig,
    start_date=date(2022,10,1),
    subgroup="A1",
    peak_contracted_demand_in_kw=250,
    off_peak_contracted_demand_in_kw=350,
)

# Formato da Tabela de Faturas: Data, peak_consumption_in_kwh, off_peak_consumption_in_kwh, peak_measured_demand_in_kw, off_peak_measured_demand_in_kw, invoice_in_reais
table_uc_campus_centro = [['2023-02-01', 20707.0, 281450.0, 538.00, 1306.62, 211121.14],
                          ['2023-03-01', 29836.0, 343275.0, 665.28, 1319.22, 237945.24],
                          ['2023-04-01', 45102.0, 365256.0, 1094.94, 1863.54, 282474.49],
                          ['2023-05-01', 49273.0, 405235.0, 1115.10, 1799.28, 306234.71],
                          ['2023-06-01', 43034.0, 363988.0, 1049.58, 1501.92, 293856.63],
                          ['2023-07-01', 36692.0, 294456.0, 946.26, 1324.26, 266057.91],
                          ['2023-08-01', 23281.0, 216430.0, 635.04, 1014.30, 209543.13],
                          ['2023-09-01', 34557.0, 278715.0, 811.44, 1326.78, 249685.69],
                          ['2023-10-01', 53644.0, 399173.0, 1278.90, 1929.06, 385557.59],
                          ['2023-11-01', 46293.0, 371087.0, 1144.40, 1842.12, 328455.38],
                          ['2023-12-01', 53072.0, 434993.0, 1362.06, 2055.06, 436850.05]]

size_campus_centro = data_size(table_uc_campus_centro)
table_uc_campus_centro = update_data(table_uc_campus_centro, size_campus_centro)
create_bills_from_table(contract2, uc_campus_centro, table_uc_campus_centro)

table_uc_campus_pampulha = [['2023-02-01', 313, 3226, 8.23, 12.77, 5260.41],
                            ['2023-03-01', 256, 2935, 7.9, 12.09, 5237.63],
                            ['2023-04-01', 275, 2810, 8.73, 10.59, 5555.83],
                            ['2023-05-01', 274, 2614, 9.07, 10.58, 5642.14],
                            ['2023-08-01', 263, 2719, 7.4, 10.25, 5776.60],
                            ['2023-09-01', 233, 2601, 7.56, 92.57, 6024.44],
                            ['2023-10-01', 341, 3424, 10.75, 76.61, 6804.60],
                            ['2023-11-01', 386, 4657, 10.92, 19.99, 6082.52],
                            ['2023-12-01', 368, 5273, 10.25, 44.69, 6571.89],
                            ['2023-01-01', 375, 4328, 10.24, 21.84, 5997.46]]

size_campus_pampulha = data_size(table_uc_campus_pampulha)
table_uc_campus_pampulha = update_data(table_uc_campus_pampulha, size_campus_pampulha)
create_bills_from_table(contract_campus_pampulha, uc_campus_pampulha, table_uc_campus_pampulha)

table_uc_montes_claros = [['2023-05-01', 7760,    66179,   156.00,  283.00, 48113.24],
                          ['2023-06-01', 4205,    53139,   154.56,  297.36, 35997.79],
                          ['2023-07-01', 5139,    63699,   171.36,  346.08, 40558.46],
                          ['2023-08-01', 13212,   85351,   288.96,  451.92, 64623.19],
                          ['2023-09-01', 12105,   80797,   285.6,   458.64, 63899.14],
                          ['2023-10-01', 15548,   97228,   295.68,  443.52, 89842.20],
                          ['2023-11-01', 12686,   85691,   268.8,   425.04, 67833.48],
                          ['2023-12-01', 6234,    57686,   184.8,   295.68, 46136.28],
                          ['2023-01-01', 15640,   99003,   344.4,   515.76, 88375.13],
                          ['2023-02-01', 17746,   225664,  366.24,  614.84, 93293.78],
                          ['2023-03-01', 20367,   135194,  403.2,   651.84, 107525.00],
                          ['2023-04-01', 11665,   83691,   268.87,  419.48, 70278.22],
                          ['2023-05-01', 13778,   117522,  281,     489.00, 85172.86],
                          ['2023-06-01', 6224,    72404,   144.48,  330.96, 55187.79],
                          ['2023-07-01', 8723,    81416,   295.68,  470.4, 63568.79],
                          ['2023-08-01', 6836,    53588,   307.44,  498.96, 44712.44],
                          ['2023-09-01', 3745,    36817,   75.6,    94.08, 32989.92],
                          ['2023-10-01', 4000,    37450,   78.96,   90.72, 34235.73],
                          ['2023-11-01', 4100,    35048,   75.6,    90.72, 32413.44],
                          ['2023-12-01', 3989,    34671,   75.6,    94.08, 32395.53]]

size_montes_claros = data_size(table_uc_montes_claros)
table_uc_montes_claros = update_data(table_uc_montes_claros, size_montes_claros)
create_bills_from_table(contract_montes_claros, uc_montes_claros, table_uc_montes_claros)

table_uc_fazenda_modelo = [['2023-05-01', 898, 10199,   19.74,   47.88,   8550.40],
                            ['2023-06-01', 971, 11605,   23.52,   34.86,   8814.11],
                            ['2023-07-01', 963, 10166,   19.32,   36.12,   8482.50],
                            ['2023-08-01', 887, 9500,    19.74,   35.28,   7877.94],
                            ['2023-09-01', 1074, 12237,   25.62,   44.52,  9681.63],
                            ['2023-10-01', 1138, 13544,   27.72,   85.68,  10692.63],
                            ['2023-11-01', 1250, 14743,   40.88,   82.39,  11217.33],
                            ['2023-12-01', 947, 11984,   43.00,    72.00,   10474.40],
                            ['2023-01-01', 996, 13717,   24.36,   70.56,   10593.53],
                            ['2023-02-01', 1049, 14011,   47.88,   101.22, 10699.28],
                            ['2023-03-01', 1139, 12552,   30.24,   43.26,  10357.78],
                            ['2023-04-01', 1030, 13562,   24.78,   46.62,  10866.41],
                            ['2023-05-01', 1123, 13315,   24.36,   46.62,  11624.41],
                            ['2023-06-01', 1107, 13776,   28.98,   58.38,  12644.44],
                            ['2023-07-01', 1170, 15270,   34.86,   69.3,   14190.70],
                            ['2023-08-01', 1196, 14873,   24.78,   73.5,   13672.60],
                            ['2023-09-01', 1404, 19833,   43.26,   109.2,  18748.05],
                            ['2023-10-01', 1376, 21105,   41.58,   110.46, 19348.38],
                            ['2023-11-01', 1564, 18567,   45.78,   94.92,  18069.45],
                            ['2023-12-01', 1631, 18668,   45.78,   98.28,  18176.20]]

size_fazenda_modelo = data_size(table_uc_fazenda_modelo)
table_uc_fazenda_modelo = update_data(table_uc_fazenda_modelo, size_fazenda_modelo)
create_bills_from_table(contract_fazenda_modelo, uc_fazenda_modelo, table_uc_fazenda_modelo)

table_uc_fazenda_experimental = [['2023-03-01', 4550, 56000, 112, 207, 8550.40],
                                 ['2023-04-01', 3500, 51100, 112, 207, 8814.11],
                                 ['2023-05-01', 4550, 51450, 112, 207, 8482.50],
                                 ['2023-06-01', 4200, 54950, 81,  179, 7877.94]]

size_fazenda_experimental = data_size(table_uc_fazenda_experimental)
table_uc_fazenda_experimental = update_data(table_uc_fazenda_experimental, size_fazenda_experimental)
create_bills_from_table(contract_fazenda_experimental, uc_fazenda_experimental, table_uc_fazenda_experimental)

table_uc_pampulha_ru_i = [['2023-10-01', 1400, 9800, 42, 67, 8550.40, False],
                          ['2023-11-01', 700, 8400, 18, 105, 8814.11, False],
                          ['2023-12-01', 1050, 8750, 35, 130, 8482.50, False],
                          ['2023-01-01', 2800, 16100, 88, 105, 7877.94, False],
                          ['2023-02-01', 3500, 18550, 116, 175, 9681.63, False],
                          ['2023-03-01', 3500, 16450, 81, 137, 10692.63, False],
                          ['2023-04-01', 2800, 12950, 77, 95, 11217.33, False],
                          ['2023-05-01', 2100, 13300, 112, 112, 10474.40, True],
                          ['2023-06-01', 3150, 16100, 74, 77, 10593.53, False],
                          ['2023-07-01', 3150, 17500, 88, 151, 10699.28, False],
                          ['2023-08-01', 4200, 21000, 130, 165, 10357.78, True],
                          ['2023-09-01', 3500, 19250, 105, 193, 10866.41, False]]

size_pampulha_ru_i = data_size(table_uc_pampulha_ru_i)
table_uc_pampulha_ru_i = update_data(table_uc_pampulha_ru_i, size_pampulha_ru_i)
create_bills_from_table(contract_pampulha_ru_i, uc_pampulha_ru_i, table_uc_pampulha_ru_i)

table_uc_pampulha_ru_ii = [['2023-12-01', 2100, 14700, 116, 126, 8550.40, False],
                           ['2023-01-01', 700, 11550, 28, 151, 8814.11, False],
                           ['2023-02-01', 2100, 15400, 0, 0, 8482.50, False],
                           ['2023-03-01', 1050, 17150, 67, 147, 7877.94, False],
                           ['2023-04-01', 3150, 18200, 119, 140, 9681.63, False],
                           ['2023-05-01', 2100, 12950, 63, 70, 10692.63, True],
                           ['2023-06-01', 1750, 13300, 116, 84, 11217.33, False],
                           ['2023-07-01', 3150, 13650, 112, 119, 9474.40, False],
                           ['2023-08-01', 3500, 16800, 144, 154, 10493.53, True],
                           ['2023-09-01', 4200, 17150, 126, 130, 10699.28, False],
                           ['2023-01-01', 3500, 18200, 175, 161, 10357.78, False]]

size_pampulha_ru_ii = data_size(table_uc_pampulha_ru_ii)
table_uc_pampulha_ru_ii = update_data(table_uc_pampulha_ru_ii, size_pampulha_ru_ii)
create_bills_from_table(contract_pampulha_ru_ii, uc_pampulha_ru_ii, table_uc_pampulha_ru_ii)

table_uc_pampulha_praca = [['2023-10-01', 1194.00, 13057.00, 62.16, 132.38, 11031.74, False],
                           ['2023-11-01', 1928.00, 20756.00, 51.74, 119.62, 15046.47, False],
                           ['2023-12-01', 5132.00, 24756.00, 174.27, 209.33, 27170.63, False],
                           ['2023-01-01', 6355.00, 27450.00, 174.05, 186.03, 29190.53, False],
                           ['2023-02-01', 5679.00, 24125.00, 168.90, 183.01, 28628.83, False],
                           ['2023-03-01', 4353.00, 16191.00, 130.59, 137.54, 21684.13, False],
                           ['2023-04-01', 1714.00, 7283.00, 94.30, 85.79, 11210.00, False],
                           ['2023-05-01', 2364.00, 9949.00, 102.93, 97.60, 13615.03, True],
                           ['2023-06-01', 4040.00, 20162.00, 167.33, 185.70, 24121.13, False],
                           ['2023-07-01', 3210.00, 19240.00, 158.82, 176.18, 21140.42, False],
                           ['2023-08-01', 4693.00, 24992.00, 190.85, 191.07, 28356.61, True],
                           ['2023-09-01', 3410.00, 21169.00, 162.74, 184.80, 23289.89, False],
                           ['2023-10-01', 702.00,  9881.00, 34.72, 88.48, 9075.88, False],
                           ['2023-11-01', 1582.00, 16121.00, 137.65, 162.51, 14690.59, False],
                           ['2023-12-01', 4169.00, 23348.00, 169.01, 167.44, 24302.93, False]]

size_pampulha_praca = data_size(table_uc_pampulha_praca)
table_uc_pampulha_praca = update_data(table_uc_pampulha_praca, size_pampulha_praca)
create_bills_from_table(contract_pampulha_praca, uc_pampulha_praca, table_uc_pampulha_praca)

table_uc_diamantina = [['2023-08-01', 949.00,  7313.00, 36.54, 75.60, 8911.80, False],
                       ['2023-09-01', 1379.00, 6980.00, 52.92, 85.18, 9518.99, False],
                       ['2023-10-01', 3226.00, 12966.00, 116.93, 116.42, 15152.39, False],
                       ['2023-11-01', 4046.00, 15832.00, 125.24, 107.10, 18368.46, False],
                       ['2023-12-01', 3062.00, 11642.00, 102.56, 106.34, 16144.65, False],
                       ['2023-01-01', 2535.00, 9259.00, 104.08, 96.01, 15217.80, False],
                       ['2023-02-01', 976.00,  5618.00, 58.21, 61.49, 9697.37, False],
                       ['2023-03-01', 1717.00, 6820.00, 65.27, 55.19, 11564.66, True],
                       ['2023-04-01', 3660.00, 12577.00, 125.75, 97.02, 18459.37, False],
                       ['2023-05-01', 3730.00, 13555.00, 106.85, 112.90, 19137.43, False],
                       ['2023-06-01', 4755.00, 18537.00, 136.84, 124.74, 23512.38, True],
                       ['2023-07-01', 3754.00, 18155.00, 142.13, 123.98, 20823.09, False],
                       ['2023-08-01', 1270.00, 8355.00, 51.91, 96.26, 10521.95, False],
                       ['2023-09-01', 1337.00, 7746.00, 60.73, 55.44, 11154.88, False],
                       ['2023-10-01', 4471.00, 15884.00, 130.03, 114.66, 20668.50, False],
                       ['2023-11-01', 601.00,  4646.00, 15.88, 24.95, 8511.99, False],
                       ['2023-12-01', 457.00,  4057.00, 11.84, 19.15, 8092.63, False],
                       ['2023-01-01', 451.00,  3413.00, 15.62, 14.62, 7920.22, False]]

size_diamantina = data_size(table_uc_diamantina)
table_uc_diamantina = update_data(table_uc_diamantina, size_diamantina)
create_bills_from_table(contract_diamantina, uc_diamantina, table_uc_diamantina)

table_uc_pampulha_teatro = [['2023-10-01', 4550, 56000, 112, 207, 8550.40],
                            ['2023-11-01', 3500, 51100, 112, 207, 8814.11],
                            ['2023-12-01', 4550, 51450, 112, 207, 8482.50]]

size_pampulha_teatro = data_size(table_uc_pampulha_teatro)
table_uc_pampulha_teatro = update_data(table_uc_pampulha_teatro, size_pampulha_teatro)
create_bills_from_table(contract_pampulha_teatro, uc_pampulha_teatro, table_uc_pampulha_teatro)

table_uc_campus_tiradentes = [['2023-05-01', 3694.00, 72646.00, 85.18,   401.18,  46297.83],
                              ['2023-06-01', 4651.00, 89642.00, 109.37,  401.69,  54043.68],
                              ['2023-07-01', 6140.00, 77351.00, 233.86,  471.24,  56991.31],
                              ['2023-08-01', 6832.00, 85369.00, 203.62,  437.47,  60971.17],
                              ['2023-09-01', 6213.00, 74501.00, 185.98,  384.05,  58810.39],
                              ['2023-10-01', 5430.00, 61454.00, 170.86,  327.60,  50843.31],
                              ['2023-11-01', 4083.00, 47109.00, 142.13,  274.68,  39178.75],
                              ['2023-12-01', 4596.00, 53172.00, 145.15,  352.80,  44265.61],
                              ['2023-01-01', 6720.00, 78688.00, 216.72,  457.63,  66738.48],
                              ['2023-02-01', 5895.00, 72789.00, 202.61,  444.02,  61028.54],
                              ['2023-03-01', 5861.00, 82537.00, 201.60,  467.71,  69004.82],
                              ['2023-04-01', 5188.00, 75373.00, 179.93,  408.74,  57292.25],
                              ['2023-05-01', 3135.00, 56690.00, 126.00,  329.62,  41744.76],
                              ['2023-06-01', 4386.00, 76257.00, 172.87,  453.10,  57713.42],
                              ['2023-07-01', 5805.00, 79273.00, 210.17,  467.71,  61630.91],
                              ['2023-08-01', 2932.00, 33611.00, 105.34,  372.46,  33835.84],
                              ['2023-09-01', 2375.00, 28034.00, 58.97,   84.17,   27939.95],
                              ['2023-10-01', 2271.00, 26297.00, 52.42,   95.76,   27255.47],
                              ['2023-11-01', 2462.00, 27517.00, 52.92,   82.15,   28072.59],
                              ['2023-12-01', 2483.00, 28673.00, 56.45,   91.73,   28894.77],
                              ['2023-01-01', 2837.00, 34244.00, 69.05,   145.66,  32447.77]]

size_campus_tiradentes = data_size(table_uc_campus_tiradentes)
table_uc_campus_tiradentes = update_data(table_uc_campus_tiradentes, size_campus_tiradentes)
create_bills_from_table(contract_campus_tiradentes, uc_campus_tiradentes, table_uc_campus_tiradentes)
