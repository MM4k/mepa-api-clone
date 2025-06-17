import unittest


class Tariff:
    def __init__(
        self,
        peak_tusd_in_reais_per_kw,
        peak_tusd_in_reais_per_mwh,
        peak_te_in_reais_per_mwh,
        off_peak_tusd_in_reais_per_kw=None,
        off_peak_tusd_in_reais_per_mwh=None,
        off_peak_te_in_reais_per_mwh=None,
        na_tusd_in_reais_per_kw=None,
    ):
        self.peak_tusd_in_reais_per_kw = peak_tusd_in_reais_per_kw
        self.peak_tusd_in_reais_per_mwh = peak_tusd_in_reais_per_mwh
        self.peak_te_in_reais_per_mwh = peak_te_in_reais_per_mwh
        self.off_peak_tusd_in_reais_per_kw = off_peak_tusd_in_reais_per_kw
        self.off_peak_tusd_in_reais_per_mwh = off_peak_tusd_in_reais_per_mwh
        self.off_peak_te_in_reais_per_mwh = off_peak_te_in_reais_per_mwh
        self.na_tusd_in_reais_per_kw = na_tusd_in_reais_per_kw


def response_tariffs_of_distributor(start_date, end_date, pending, blue_tariff, green_tariff):
    response_blue = None
    response_green = None

    if blue_tariff:
        response_blue = {
            "peakTusdInReaisPerKw": blue_tariff.peak_tusd_in_reais_per_kw,
            "peakTusdInReaisPerMwh": blue_tariff.peak_tusd_in_reais_per_mwh,
            "peakTeInReaisPerMwh": blue_tariff.peak_te_in_reais_per_mwh,
            "offPeakTusdInReaisPerKw": blue_tariff.off_peak_tusd_in_reais_per_kw,
            "offPeakTusdInReaisPerMwh": blue_tariff.off_peak_tusd_in_reais_per_mwh,
            "offPeakTeInReaisPerMwh": blue_tariff.off_peak_te_in_reais_per_mwh,
        }

    if green_tariff:
        response_green = {
            "peakTusdInReaisPerMwh": green_tariff.peak_tusd_in_reais_per_mwh,
            "peakTeInReaisPerMwh": green_tariff.peak_te_in_reais_per_mwh,
            "offPeakTusdInReaisPerMwh": green_tariff.off_peak_tusd_in_reais_per_mwh,
            "offPeakTeInReaisPerMwh": green_tariff.off_peak_te_in_reais_per_mwh,
            "naTusdInReaisPerKw": green_tariff.na_tusd_in_reais_per_kw,
        }

    return {
        "start_date": start_date,
        "end_date": end_date,
        "overdue": pending,
        "blue": response_blue,
        "green": response_green,
    }


class TestResponseTariffsOfDistributor(unittest.TestCase):
    def test_no_tariffs(self):
        result = response_tariffs_of_distributor("2023-01-01", "2023-12-31", True, None, None)
        expected = {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "overdue": True,
            "blue": None,
            "green": None,
        }
        self.assertEqual(result, expected)

    def test_blue_tariff_only(self):
        blue_tariff = Tariff(100, 200, 300, 50, 150, 250)
        result = response_tariffs_of_distributor("2023-01-01", "2023-12-31", False, blue_tariff, None)
        expected = {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "overdue": False,
            "blue": {
                "peakTusdInReaisPerKw": 100,
                "peakTusdInReaisPerMwh": 200,
                "peakTeInReaisPerMwh": 300,
                "offPeakTusdInReaisPerKw": 50,
                "offPeakTusdInReaisPerMwh": 150,
                "offPeakTeInReaisPerMwh": 250,
            },
            "green": None,
        }
        self.assertEqual(result, expected)

    def test_green_tariff_only(self):
        green_tariff = Tariff(150, 250, 350, None, None, None, 100)
        result = response_tariffs_of_distributor("2023-01-01", "2023-12-31", False, None, green_tariff)
        expected = {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "overdue": False,
            "blue": None,
            "green": {
                "peakTusdInReaisPerMwh": 250,
                "peakTeInReaisPerMwh": 350,
                "offPeakTusdInReaisPerMwh": 250,
                "offPeakTeInReaisPerMwh": 350,
                "naTusdInReaisPerKw": 100,
            },
        }
        self.assertEqual(result, expected)

    def test_both_tariffs(self):
        blue_tariff = Tariff(100, 200, 300, 50, 150, 250)
        green_tariff = Tariff(150, 250, 350, None, None, None, 100)
        result = response_tariffs_of_distributor("2023-01-01", "2023-12-31", False, blue_tariff, green_tariff)
        expected = {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "overdue": False,
            "blue": {
                "peakTusdInReaisPerKw": 100,
                "peakTusdInReaisPerMwh": 200,
                "peakTeInReaisPerMwh": 300,
                "offPeakTusdInReaisPerKw": 50,
                "offPeakTusdInReaisPerMwh": 150,
                "offPeakTeInReaisPerMwh": 250,
            },
            "green": {
                "peakTusdInReaisPerMwh": 250,
                "peakTeInReaisPerMwh": 350,
                "offPeakTusdInReaisPerMwh": 250,
                "offPeakTeInReaisPerMwh": 350,
                "naTusdInReaisPerKw": 100,
            },
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
