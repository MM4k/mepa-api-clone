from datetime import date

import pytest

from utils.tariff_util import response_tariffs_of_distributor


class Tariff:
    def __init__(
        self,
        peak_tusd_in_reais_per_kw,
        peak_tusd_in_reais_per_mwh,
        peak_te_in_reais_per_mwh,
        off_peak_tusd_in_reais_per_kw,
        off_peak_tusd_in_reais_per_mwh,
        off_peak_te_in_reais_per_mwh,
        na_tusd_in_reais_per_kw,
    ):
        self.peak_tusd_in_reais_per_kw = peak_tusd_in_reais_per_kw
        self.peak_tusd_in_reais_per_mwh = peak_tusd_in_reais_per_mwh
        self.peak_te_in_reais_per_mwh = peak_te_in_reais_per_mwh
        self.off_peak_tusd_in_reais_per_kw = off_peak_tusd_in_reais_per_kw
        self.off_peak_tusd_in_reais_per_mwh = off_peak_tusd_in_reais_per_mwh
        self.off_peak_te_in_reais_per_mwh = off_peak_te_in_reais_per_mwh
        self.na_tusd_in_reais_per_kw = na_tusd_in_reais_per_kw


def test_response_with_blue_tariff_only():
    blue_tariff = Tariff(
        peak_tusd_in_reais_per_kw=1.2,
        peak_tusd_in_reais_per_mwh=3.4,
        peak_te_in_reais_per_mwh=5.6,
        off_peak_tusd_in_reais_per_kw=0.7,
        off_peak_tusd_in_reais_per_mwh=2.1,
        off_peak_te_in_reais_per_mwh=4.3,
        na_tusd_in_reais_per_kw=None,
    )
    green_tariff = None
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    pending = False

    result = response_tariffs_of_distributor(start_date, end_date, pending, blue_tariff, green_tariff)

    assert result["blue"] is not None
    assert result["blue"]["peakTusdInReaisPerKw"] == 1.2
    assert result["blue"]["peakTusdInReaisPerMwh"] == 3.4
    assert result["blue"]["peakTeInReaisPerMwh"] == 5.6
    assert result["blue"]["offPeakTusdInReaisPerKw"] == 0.7
    assert result["blue"]["offPeakTusdInReaisPerMwh"] == 2.1
    assert result["blue"]["offPeakTeInReaisPerMwh"] == 4.3
    assert result["green"] is None


def test_response_with_green_tariff_only():
    blue_tariff = None
    green_tariff = Tariff(
        peak_tusd_in_reais_per_kw=None,
        peak_tusd_in_reais_per_mwh=3.4,
        peak_te_in_reais_per_mwh=5.6,
        off_peak_tusd_in_reais_per_kw=None,
        off_peak_tusd_in_reais_per_mwh=2.1,
        off_peak_te_in_reais_per_mwh=4.3,
        na_tusd_in_reais_per_kw=0.7,
    )
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    pending = False

    result = response_tariffs_of_distributor(start_date, end_date, pending, blue_tariff, green_tariff)

    assert result["green"] is not None
    assert result["green"]["peakTusdInReaisPerMwh"] == 3.4
    assert result["green"]["peakTeInReaisPerMwh"] == 5.6
    assert result["green"]["offPeakTusdInReaisPerMwh"] == 2.1
    assert result["green"]["offPeakTeInReaisPerMwh"] == 4.3
    assert result["green"]["naTusdInReaisPerKw"] == 0.7
    assert result["blue"] is None


def test_response_with_both_tariffs():
    blue_tariff = Tariff(
        peak_tusd_in_reais_per_kw=1.2,
        peak_tusd_in_reais_per_mwh=3.4,
        peak_te_in_reais_per_mwh=5.6,
        off_peak_tusd_in_reais_per_kw=0.7,
        off_peak_tusd_in_reais_per_mwh=2.1,
        off_peak_te_in_reais_per_mwh=4.3,
        na_tusd_in_reais_per_kw=None,
    )
    green_tariff = Tariff(
        peak_tusd_in_reais_per_kw=None,
        peak_tusd_in_reais_per_mwh=3.4,
        peak_te_in_reais_per_mwh=5.6,
        off_peak_tusd_in_reais_per_kw=None,
        off_peak_tusd_in_reais_per_mwh=2.1,
        off_peak_te_in_reais_per_mwh=4.3,
        na_tusd_in_reais_per_kw=0.7,
    )
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    pending = True

    result = response_tariffs_of_distributor(start_date, end_date, pending, blue_tariff, green_tariff)

    assert result["blue"] is not None
    assert result["green"] is not None
    assert result["blue"]["peakTusdInReaisPerKw"] == 1.2
    assert result["green"]["naTusdInReaisPerKw"] == 0.7
    assert result["start_date"] == start_date
    assert result["end_date"] == end_date
    assert result["overdue"] == pending


def test_response_with_no_tariffs():
    blue_tariff = None
    green_tariff = None
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    pending = False

    result = response_tariffs_of_distributor(start_date, end_date, pending, blue_tariff, green_tariff)

    assert result["blue"] is None
    assert result["green"] is None
