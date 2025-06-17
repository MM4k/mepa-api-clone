import pytest

from tests.test_utils import create_objects_test_utils, dicts_test_utils


@pytest.mark.django_db
class TestTariff:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.university = create_objects_test_utils.create_test_university(self.university_dict)

        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)

    def test_create_blue_tariff(self):
        tariff_dict = dicts_test_utils.tariff_dict_1
        tariff = create_objects_test_utils.create_test_blue_tariff(tariff_dict, self.distributor)

        assert tariff.is_blue()

        blue_tariff = tariff.as_blue_tariff()

        assert 1 == blue_tariff.peak_tusd_in_reais_per_kw
        assert 4 == blue_tariff.off_peak_tusd_in_reais_per_kw

    def test_create_green_tariff(self):
        tariff_dict = dicts_test_utils.tariff_dict_1
        tariff = create_objects_test_utils.create_test_green_tariff(tariff_dict, self.distributor)

        assert tariff.is_green()

        green_tariff = tariff.as_green_tariff()

        assert 2 == green_tariff.peak_tusd_in_reais_per_mwh
        assert 7 == green_tariff.na_tusd_in_reais_per_kw

    def test_mishandles_green_tariff_as_blue_tariff(self):
        tariff_dict = dicts_test_utils.tariff_dict_1
        tariff = create_objects_test_utils.create_test_green_tariff(tariff_dict, self.distributor)

        with pytest.raises(Exception) as e:
            tariff.as_blue_tariff()
        assert "Cannot convert" in str(e.value)

    def test_mishandles_blue_tariff_as_green_tariff(self):
        tariff_dict = dicts_test_utils.tariff_dict_1
        tariff = create_objects_test_utils.create_test_blue_tariff(tariff_dict, self.distributor)

        with pytest.raises(Exception) as e:
            tariff.as_green_tariff()
        assert "Cannot convert" in str(e.value)

    def test_create_tariff_with_invalid_data(self):
        invalid_tariff_dict = {"invalid_field": "invalid_value"}

        with pytest.raises(Exception) as e:
            create_objects_test_utils.create_test_blue_tariff(invalid_tariff_dict, self.distributor)
        assert "subgroup" in str(e.value)
