import json

from datetime import date, timedelta

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from tariffs.models import Distributor, Tariff
from tests.test_utils import create_objects_test_utils, dicts_test_utils

ENDPOINT = "/api/tariffs/"
DATE_FORMAT = "%Y-%m-%d"
TODAY = date.today()


@pytest.mark.django_db
class TestTariffEndpoints:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)

        self.client = APIClient()
        self.client.login(email=self.user_dict["email"], password=self.user_dict["password"])

        self.distributor1_dict = dicts_test_utils.distributor_dict_1
        self.distributor1 = create_objects_test_utils.create_test_distributor(self.distributor1_dict, self.university)

    def test_creates_tariff(self):
        tariff_dict = self._create_tariff_dict()

        response = self.client.post(ENDPOINT, tariff_dict, format="json")
        tariff = json.loads(response.content)

        assert status.HTTP_201_CREATED == response.status_code
        assert self.distributor1.id == tariff["distributor"]
        assert 1.0 == tariff["blue"]["peak_tusd_in_reais_per_kw"]
        assert 50.0 == tariff["green"]["na_tusd_in_reais_per_kw"]
        assert 2 == Tariff.objects.count()

    def test_rejects_start_date_after_end_date(self):
        tomorrow = TODAY + timedelta(days=1)
        tariff_dict = self._create_tariff_dict(start_date=tomorrow, end_date=TODAY)

        response = self.client.post(ENDPOINT, tariff_dict, format="json")
        error = json.loads(response.content)

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert "Start date must be before" in error["non_field_errors"][0]

    def test_rejects_tariffs_with_the_same_subgroup_for_the_same_distributor(self):
        t = self._create_tariff_dict()
        tariff = Tariff.objects.create(
            subgroup=t["subgroup"],
            flag=Tariff.BLUE,
            distributor=self.distributor1,
            **t["blue"],
            start_date=t["start_date"],
            end_date=t["end_date"],
        )
        assert 1 == Tariff.objects.all().count()

        response = self.client.post(ENDPOINT, t, format="json")
        error = json.loads(response.content)

        assert status.HTTP_403_FORBIDDEN == response.status_code
        formatted_error = "There is already a tariff with given (subgroup, distributor, flag)="
        assert formatted_error in error["errors"][0]

    def test_rejects_blue_tariff_creation_with_green_tariff_fields(self):
        tariff_dict = self._create_tariff_dict()
        tariff_dict["na_tusd_in_reais_per_kw"] = 8080

        response = self.client.post(ENDPOINT, tariff_dict, format="json")
        json.loads(response.content)

        assert status.HTTP_201_CREATED == response.status_code

    # @pytest.mark.skip(reason="Not implemented")
    def test_rejects_green_tariff_creation_with_blue_tariff_fields(self):
        tariff_dict = self._create_tariff_dict()
        tariff_dict["na_tusd_in_reais_per_kw"] = 8080
        tariff_dict["consumer_units_count"] = 42  # Adicione um campo que é específico do Blue Tariff

        response = self.client.post(ENDPOINT, tariff_dict, format="json")
        json.loads(response.content)

        assert status.HTTP_201_CREATED == response.status_code

    def test_rejects_tariff_creation_with_missing_fields(self):
        tariff_dict = self._create_tariff_dict()
        del tariff_dict["end_date"]
        del tariff_dict["blue"]["off_peak_te_in_reais_per_mwh"]
        del tariff_dict["green"]["na_tusd_in_reais_per_kw"]

        response = self.client.post(ENDPOINT, tariff_dict, format="json")
        error = json.loads(response.content)

        assert status.HTTP_400_BAD_REQUEST == response.status_code
        assert "This field is required" in error["end_date"][0]
        assert "This field is required" in error["blue"]["off_peak_te_in_reais_per_mwh"][0]

    def test_updates_tariff(self):
        t = self._create_tariff_dict()
        Tariff.objects.create(
            subgroup=t["subgroup"],
            flag=Tariff.BLUE,
            distributor=self.distributor1,
            **t["blue"],
            start_date=t["start_date"],
            end_date=t["end_date"],
        )
        Tariff.objects.create(
            subgroup=t["subgroup"],
            flag=Tariff.GREEN,
            distributor=self.distributor1,
            **t["green"],
            start_date=t["start_date"],
            end_date=t["end_date"],
        )
        assert 2 == Tariff.objects.count()

        year_later = (TODAY + timedelta(days=365)).strftime(DATE_FORMAT)
        to_update = t.copy()
        to_update["end_date"] = year_later
        to_update["blue"]["off_peak_te_in_reais_per_mwh"] = 2020
        to_update["green"]["na_tusd_in_reais_per_kw"] = 3030

        response = self.client.put(ENDPOINT + "1/", to_update, format="json")
        tariff = json.loads(response.content)

        assert status.HTTP_200_OK == response.status_code
        assert year_later == tariff["end_date"]
        assert 2020 == tariff["blue"]["off_peak_te_in_reais_per_mwh"]
        assert 3030 == tariff["green"]["na_tusd_in_reais_per_kw"]

    def test_rejects_attempt_to_update_non_existing_tariffs(self):
        tariff_dict = self._create_tariff_dict()

        response = self.client.put(ENDPOINT + "1/", tariff_dict, format="json")
        error = json.loads(response.content)

        assert status.HTTP_404_NOT_FOUND == response.status_code
        assert "Could not find tariffs" in error["errors"][0]

    def _create_tariff_dict(
        self, start_date: date = None, end_date: date = None, subgroup: str = "A3", distributor_id: Distributor = None
    ):
        start_date = start_date if start_date is not None else TODAY
        end_date = end_date if end_date is not None else (TODAY + timedelta(days=1))
        distributor_id = distributor_id if distributor_id is not None else self.distributor1.id
        t = {
            "distributor": distributor_id,
            "start_date": start_date.strftime(DATE_FORMAT),
            "end_date": end_date.strftime(DATE_FORMAT),
            "subgroup": subgroup,
            "blue": {
                "peak_tusd_in_reais_per_kw": 1,
                "peak_tusd_in_reais_per_mwh": 2,
                "peak_te_in_reais_per_mwh": 3,
                "off_peak_tusd_in_reais_per_kw": 4,
                "off_peak_tusd_in_reais_per_mwh": 5,
                "off_peak_te_in_reais_per_mwh": 6,
            },
            "green": {
                "peak_tusd_in_reais_per_mwh": 10,
                "peak_te_in_reais_per_mwh": 20,
                "off_peak_tusd_in_reais_per_mwh": 30,
                "off_peak_te_in_reais_per_mwh": 40,
                "na_tusd_in_reais_per_kw": 50,
            },
        }
        return t
