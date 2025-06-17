from datetime import date

from django.db import models
from django.utils.translation import gettext_lazy as _

from contracts.models import Contract, EnergyBill
from utils.energy_bill_util import EnergyBillUtils

from .recommendation import Recommendation


class University(models.Model):
    class Meta:
        verbose_name_plural = "Universities"

    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_("Nome"),
        help_text=_("Nome da universidade por extenso"),
    )

    acronym = models.CharField(
        null=True,
        max_length=50,
        unique=True,
        verbose_name=_("Sigla"),
        help_text=_("Exemplo: UnB, UFSC, UFB"),
    )

    cnpj = models.CharField(
        max_length=14,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_("CNPJ"),
        help_text=_("14 números sem caracteres especiais"),
    )

    is_active = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.acronym} - {self.name}"


class ConsumerUnit(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nome"),
        help_text=_("Nome da Unidade Consumidora. Ex: Darcy Ribeiro"),
    )

    code = models.CharField(
        max_length=30,
        verbose_name=_("Código da Unidade Consumidora"),
        help_text=_("Cheque a conta de luz para obter o código da Unidade Consumidora. Insira apenas números"),
    )

    university = models.ForeignKey(
        University,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        verbose_name="Universidade",
        related_name="consumer_units",
        help_text=_("Uma Unidade Consumidora deve estar ligada a uma Universidade"),
    )

    total_installed_power = models.DecimalField(
        decimal_places=2,
        max_digits=7,
        null=True,
        blank=True,
        help_text=_("Potência total de geração de energia instalada em kw"),
    )

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["university", "code"], name="unique_consumer_unit_university_code"),
            models.UniqueConstraint(fields=["university", "name"], name="unique_consumer_unit_university_name"),
        ]

    def __str__(self):
        return f"{self.name} - {self.code}"

    @property
    def current_contract(self) -> Contract:
        return self.contract_set.all().order_by("start_date").last()

    @property
    def oldest_contract(self) -> Contract:
        return self.contract_set.all().order_by("start_date").first()

    @property
    def previous_contract(self) -> Contract:
        if self.current_contract is None:
            return None

        return self.contract_set.filter(start_date__lt=self.current_contract.start_date).order_by("start_date").last()

    @property
    def date(self):
        return self.oldest_contract.start_date

    @property
    def is_current_energy_bill_filled(self):
        if EnergyBill.get_energy_bill(self.id, date.today().month, date.today().year):
            return True
        return False

    @property
    def pending_energy_bills_number(self):
        return len(self.get_energy_bills_pending())

    @classmethod
    def check_insert_is_favorite_on_consumer_units(cls, consumer_unit_list, user_id):
        from users.models import UniversityUser

        updated_consumer_unit_list = []
        university_user: UniversityUser = UniversityUser.objects.get(id=user_id)

        for unit in consumer_unit_list:
            unit_dict = dict(unit)
            unit_dict["is_favorite"] = university_user.check_if_consumer_unit_is_your_favorite(unit_dict["id"])

            updated_consumer_unit_list.append(unit_dict)

        return updated_consumer_unit_list

    def get_energy_bills_by_year(self, year):
        if year < self.date.year or year > date.today().year:
            raise Exception("Consumer User do not have Energy Bills this year")

        energy_bills_dates = EnergyBillUtils.generate_dates_by_year(year)

        for energy_bill_date in energy_bills_dates:
            energy_bill_date["energy_bill"] = None
            energy_bill = EnergyBill.get_energy_bill(self.id, energy_bill_date["month"], energy_bill_date["year"])

            if energy_bill:
                energy_bill_date["energy_bill"] = EnergyBillUtils.energy_bill_dictionary(energy_bill)

        return list(energy_bills_dates)

    def get_energy_bills_pending(self):
        energy_bills_pending = []
        energy_bills = self.get_energy_bills_for_recommendation()

        for energy_bill in energy_bills:
            energy_bill_date = date(energy_bill["year"], energy_bill["month"], 1)

            if energy_bill_date >= self.oldest_contract.start_date:
                if energy_bill["energy_bill"] is None:
                    energy_bills_pending.append(energy_bill)

        return list(energy_bills_pending)

    def get_energy_bills_for_recommendation(self):
        return Recommendation.get_energy_bills_for_recommendation(self.id)

    def get_all_energy_bills(self):
        return Recommendation.get_all_energy_bills_by_consumer_unit(self.id, self.date)

    def __repr__(self) -> str:
        return f"UC {self.name}"
