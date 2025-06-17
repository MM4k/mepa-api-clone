from tests.recommendation.readcsv import CsvData, CsvReader

# Os casos de teste estão em recommendation/tests/data/uc_{code}/**
# Esses code's devem entrar na lista abaixo:
consumer_units_codes = [
    "1011101-5",
    # '9006211',
]


def __setup_test_cases():
    readers = [CsvReader(code) for code in consumer_units_codes]
    datas = [reader.run() for reader in readers]

    test_cases: dict[str, CsvData] = {}
    for code, data in zip(consumer_units_codes, datas):
        test_cases[code] = data

    return test_cases


test_cases = __setup_test_cases()
