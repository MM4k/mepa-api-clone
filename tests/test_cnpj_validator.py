import pytest

from utils.cnpj_validator_util import CnpjValidator


def test_valid_cnpj():
    valid_cnpjs = [
        "11222333000181",
        "12345678000195",
    ]
    for cnpj in valid_cnpjs:
        try:
            CnpjValidator.validate(cnpj)
        except Exception as e:
            pytest.fail(f"Valid CNPJ '{cnpj}' failed validation with exception: {e}")


def test_invalid_cnpj():
    invalid_cnpjs = [
        "00000000000000",
        "11222333000182",
        "43.285.565/0001-71",
    ]
    for cnpj in invalid_cnpjs:
        with pytest.raises(Exception):
            CnpjValidator.validate(cnpj)


def test_invalid_format():
    invalid_formats = [
        "123",
        "abcdefghijlmn",
        "123456789012345",
    ]
    for cnpj in invalid_formats:
        with pytest.raises(Exception):
            CnpjValidator.validate(cnpj)


def test_zeroed_cnpj():
    with pytest.raises(Exception):
        CnpjValidator.validate("00000000000001")


def test_direct_verify_digit():
    base_digits_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
    expected_digit_1 = calculate_expected_digit(CnpjValidator.multipliers_1, base_digits_1)
    assert CnpjValidator._verify_digit(CnpjValidator.multipliers_1, base_digits_1) == expected_digit_1

    base_digits_2 = [3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    expected_digit_2 = calculate_expected_digit(CnpjValidator.multipliers_2, base_digits_2)
    assert CnpjValidator._verify_digit(CnpjValidator.multipliers_2, base_digits_2) == expected_digit_2


def calculate_expected_digit(multipliers, base_digits):
    sum_result = sum(m * b for m, b in zip(multipliers, base_digits))
    mod_result = sum_result % 11
    return 0 if mod_result < 2 else 11 - mod_result
