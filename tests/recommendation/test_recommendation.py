import pytest

from pandas.testing import assert_frame_equal

from recommendation.calculator import RecommendationCalculator
from tests.recommendation.test_cases import test_cases

test_data = [(code) for code in test_cases.keys()]

ABSOLUTE_TOLERANCE = 0.01


@pytest.mark.parametrize("code", test_data)
def test_recommendation(code: str):
    data = test_cases[code]
    sut = RecommendationCalculator(
        data.consumption_history,
        data.current_tariff_flag,
        data.blue_tariff,
        data.green_tariff,
        "A4",
        None,
    )

    result = sut.calculate(None)

    assert_frame_equal(
        data.expected_current_contract,
        result.current_contract,
        check_exact=False,
        atol=ABSOLUTE_TOLERANCE,
    )

    assert data.expected_recommended_tariff_flag == result.tariff_flag

    assert_frame_equal(
        data.expected_recommendation,
        result.frame,
        check_exact=False,
        atol=ABSOLUTE_TOLERANCE,
    )
