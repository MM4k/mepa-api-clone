from datetime import date, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from django.db import models, transaction

from utils.date_util import DateUtils
from utils.energy_bill_util import EnergyBillUtils


class ContractManager(models.Manager):
    def create(self, *args, **kwargs):
        with transaction.atomic():
            try:
                obj = self.model(*args, **kwargs)
                obj.check_start_date_create_contract()
                obj.save()
                obj.set_last_contract_end_date()
            except Exception as e:
                raise e
            return obj


class Contract(models.Model):
    tariff_flag_choices = (
        ("G", "Verde"),
        ("B", "Azul"),
    )

    subgroup_choices = (
        ("A1", "≥ 230 kV"),
        ("A2", "de 88 kV a 138 kV"),
        ("A3", "de 69 kV"),
        ("A3a", "de 30 kV a 44 kV"),
        ("A4", "de 2,3 kV a 25 kV"),
        ("AS", "< a 2,3 kV, a partir de sistema subterrâneo de distribuição"),
    )

    consumer_unit = models.ForeignKey("universities.ConsumerUnit", on_delete=models.PROTECT)
    distributor = models.ForeignKey("tariffs.Distributor", related_name="contracts", on_delete=models.PROTECT)
    start_date = models.DateField(default=date.today, null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)
    tariff_flag = models.CharField(choices=tariff_flag_choices, max_length=1, null=True, blank=True)
    subgroup = models.CharField(choices=subgroup_choices, max_length=3, null=True, blank=True)
    peak_contracted_demand_in_kw = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    off_peak_contracted_demand_in_kw = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)

    objects = ContractManager()

    def __str__(self):
        return f"{self.distributor.name} - {self.distributor.university.acronym} ({self.start_date})"

    def check_start_date_create_contract(self):
        if self.consumer_unit.current_contract:
            if self.start_date <= self.consumer_unit.current_contract.start_date:
                raise Exception(
                    self.start_date,
                    self.consumer_unit.current_contract.start_date,
                    "Novo Contrato não pode ter uma data anterior ou igual ao Contrato atual",
                )

    def check_start_date_edit_contract(self):
        if self.consumer_unit.previous_contract:
            if self.consumer_unit.previous_contract != self.consumer_unit.current_contract:
                if self.start_date < self.consumer_unit.previous_contract.start_date:
                    raise Exception("Contrato não pode ser editado com a data anterior ao ultimo Contrato")

    def check_start_date_is_valid(self):
        if self.end_date:
            return

        consumer_unit = self.consumer_unit

        if consumer_unit.current_contract:
            if (
                self.start_date >= consumer_unit.oldest_contract.start_date
                and self.start_date < consumer_unit.current_contract.start_date
            ):
                raise Exception("Already have the contract in this date")

    def check_tariff_flag_is_valid(self):
        if self.tariff_flag == "G" and self.subgroup in ("A2", "A3"):
            raise Exception("Contrato não pode ter tensão equivalente aos subgrupos A2 ou A3 e ser modalidade Verde")

    def set_last_contract_end_date(self):
        day_before_start_date = DateUtils.get_yesterday_date(self.start_date)

        if self.consumer_unit.previous_contract:
            previous_contract = self.consumer_unit.previous_contract
            previous_contract.end_date = day_before_start_date
            previous_contract.save()

    def get_distributor_name(self):
        return self.distributor.name


class EnergyBill(models.Model):
    contract = models.ForeignKey("Contract", on_delete=models.PROTECT)
    consumer_unit = models.ForeignKey("universities.ConsumerUnit", on_delete=models.PROTECT)
    date = models.DateField(null=True, blank=True)
    is_atypical = models.BooleanField(default=False)
    anotacoes = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    invoice_in_reais = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    off_peak_consumption_in_kwh = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    peak_measured_demand_in_kw = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    off_peak_measured_demand_in_kw = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    peak_consumption_in_kwh = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    energy_bill_file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "ppt", "xlsx", "png", "jpg", "jpeg"])],
        max_length=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.consumer_unit} - {self.date}"

    def save(self, *args, **kwargs):
        if not isinstance(self.date, date):
            try:
                self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato de data inválido. Por favor use 'YYYY-MM-DD'.")
        if self.date > date.today():
            raise Exception("A data da fatura não pode ser posterior à data atual.")

        if self.date < self.consumer_unit.oldest_contract.start_date:
            raise Exception("A data da fatura não pode ser anterior à data de início do contrato mais antigo.")

        if not EnergyBillUtils.check_valid_consumption_demand(self):
            raise Exception("O campo de consumo e demanda não pode ser 0.")

        existing_energy_bill = (
            EnergyBill.objects.filter(
                consumer_unit=self.consumer_unit,
                date__year=self.date.year,
                date__month=self.date.month,
            )
            .exclude(id=self.id)
            .exists()
        )

        if existing_energy_bill:
            raise Exception("Já existe uma fatura cadastrada para este mês.")

        super().save(*args, **kwargs)

    @classmethod
    def get_energy_bill(cls, consumer_unit_id, month, year):
        try:
            return cls.objects.get(
                consumer_unit=consumer_unit_id,
                date__month=month,
                date__year=year,
            )
        except ObjectDoesNotExist:
            return None
        except Exception as error:
            raise Exception(f"Get Energy Bill: {str(error)}")

    @classmethod
    def check_energy_bill_month_year(cls, consumer_unit_id, energy_bill_date):
        has_already_energy_bill = EnergyBill.objects.filter(
            consumer_unit=consumer_unit_id,
            date__year=energy_bill_date.year,
            date__month=energy_bill_date.month,
        ).exists()

        return has_already_energy_bill

    def check_energy_bill_covered_by_contract(consumer_unit_id, energy_bill_date):
        oldest_contract = Contract.objects.filter(consumer_unit=consumer_unit_id).order_by("start_date").first()
        latest_contract = Contract.objects.filter(consumer_unit=consumer_unit_id).order_by("-start_date").first()

        if oldest_contract and latest_contract:
            if energy_bill_date >= oldest_contract.start_date or energy_bill_date >= latest_contract.start_date:
                return True, None
            return False, max(oldest_contract.start_date, latest_contract.start_date)
        return False, None
