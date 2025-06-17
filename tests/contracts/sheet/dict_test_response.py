invalid_date_format_dict = {
    "data": [
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": [
                    [
                        8,
                        'O mês deve ser uma data nos formatos "mm/aaaa", "mmm/aaaa" como "abr/2024"',
                    ]
                ],
                "value": "04-2024",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 3245.77,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": 325,
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 350,
            },
            "peak_consumption_in_kwh": {
                "errors": None,
                "value": 325,
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 350,
            },
        },
    ],
}

invalid_header_dict = {
    "file": [
        "\"['Data', 'Valor (R$)', 'Consumo Ponta (kWh)', 'Consumo Fora "
        "Ponta (kWh)', 'Demanda Ponta (kW)', 'Demanda Fora Ponta (kW)'] not "
        'found in axis"',
    ],
}

invalid_date_all_dict = {
    "data": [
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": None,
                "value": "2024-04-01",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 3245.77,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": 325,
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 350,
            },
            "peak_consumption_in_kwh": {
                "errors": None,
                "value": 325,
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 350,
            },
        },
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": [
                    [
                        7,
                        "Selecione uma data a partir de Janeiro de 2021. Não "
                        "existem contratos registrados antes disso.",
                    ],
                ],
                "value": "2020-04-01",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 2312.11,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": 350,
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 325,
            },
            "peak_consumption_in_kwh": {
                "errors": None,
                "value": 350,
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 325,
            },
        },
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": [
                    [
                        10,
                        "Já existe uma fatura lançada neste mês",
                    ],
                ],
                "value": "2024-08-01",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 4512.12,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": 370,
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 230,
            },
            "peak_consumption_in_kwh": {
                "errors": None,
                "value": 320,
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 123,
            },
        },
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": [
                    [
                        10,
                        "Já existe uma fatura lançada neste mês",
                    ],
                    [
                        6,
                        "Este mês está duplicado na planilha",
                    ],
                ],
                "value": "2024-08-01",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 1823.97,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": 370,
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 230,
            },
            "peak_consumption_in_kwh": {
                "errors": None,
                "value": 350,
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 123,
            },
        },
    ],
}

invalid_number_dict_xlsx = {
    "data": [
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": None,
                "value": "2024-04-01",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 218.55,
            },
            "off_peak_consumption_in_kwh": {
                "errors": [
                    [
                        9,
                        "Valores de Consumo e Demanda devem ser números entre 0,1 e 9.999.999,99",
                    ],
                ],
                "value": "abd",
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 412,
            },
            "peak_consumption_in_kwh": {
                "errors": None,
                "value": 24,
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 350,
            },
        },
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": [
                    [
                        8,
                        'O mês deve ser uma data nos formatos "mm/aaaa", "mmm/aaaa" como "abr/2024"',
                    ],
                ],
                "value": "05-2024",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 8371.22,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": 35,
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 55,
            },
            "peak_consumption_in_kwh": {
                "errors": [
                    [
                        9,
                        "Valores de Consumo e Demanda devem ser números entre 0,1 e 9.999.999,99",
                    ],
                ],
                "value": 10000000000,
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 21,
            },
        },
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": None,
                "value": "2021-08-01",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 874.4,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": 23,
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 231,
            },
            "peak_consumption_in_kwh": {
                "errors": [
                    [
                        9,
                        "Valores de Consumo e Demanda devem ser números entre 0,1 e 9.999.999,99",
                    ],
                ],
                "value": "pedro",
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 135,
            },
        },
    ],
}

invalid_number_dict_csv = {
    "data": [
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": None,
                "value": "2024-04-01",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 218.55,
            },
            "off_peak_consumption_in_kwh": {
                "errors": [
                    [
                        9,
                        "Valores de Consumo e Demanda devem ser números entre 0,1 e 9.999.999,99",
                    ],
                ],
                "value": "abd",
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 412,
            },
            "peak_consumption_in_kwh": {
                "errors": None,
                "value": "24",
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 350,
            },
        },
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": [
                    [
                        8,
                        'O mês deve ser uma data nos formatos "mm/aaaa", "mmm/aaaa" como "abr/2024"',
                    ],
                ],
                "value": "05-2024",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 8371.22,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": "35",
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 55,
            },
            "peak_consumption_in_kwh": {
                "errors": [
                    [
                        9,
                        "Valores de Consumo e Demanda devem ser números entre 0,1 e 9.999.999,99",
                    ],
                ],
                "value": "10000000000",
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 21,
            },
        },
        {
            "consumer_unit": {
                "error": False,
                "value": 1,
            },
            "date": {
                "errors": None,
                "value": "2021-08-01",
            },
            "invoice_in_reais": {
                "errors": None,
                "value": 874.4,
            },
            "off_peak_consumption_in_kwh": {
                "errors": None,
                "value": "23",
            },
            "off_peak_measured_demand_in_kw": {
                "errors": None,
                "value": 231,
            },
            "peak_consumption_in_kwh": {
                "errors": [
                    [
                        9,
                        "Valores de Consumo e Demanda devem ser números entre 0,1 e 9.999.999,99",
                    ],
                ],
                "value": "pedro",
            },
            "peak_measured_demand_in_kw": {
                "errors": None,
                "value": 135,
            },
        },
    ],
}
