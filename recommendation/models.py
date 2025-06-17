from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class Recommendation(models.Model):
    consumer_unit = models.OneToOneField(
        "universities.ConsumerUnit",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    isValid = models.BooleanField(null=True, blank=True)
    currentContract = models.ForeignKey("contracts.Contract", on_delete=models.CASCADE, null=True)
    generatedOn = models.DateTimeField(default=timezone.now)
    energyBillsCount = models.IntegerField(null=True, blank=True)
    currentTotalCost = models.FloatField(null=True, blank=True)
    shouldRenewContract = models.BooleanField(null=True, blank=True)
    nominalSavingsPercentage = models.FloatField(null=True, blank=True)
    dates = ArrayField(models.DateField(), null=True)
    errors = models.JSONField(null=True)
    warnings = models.JSONField(null=True)
    tariffStartDate = models.DateField(null=True)
    tariffEndDate = models.DateField(null=True)
    costsComparisonPlot = models.JSONField(null=True)
    recommendedContract = models.JSONField(null=True)
    currentContractCostsPlot = models.JSONField(null=True)
    contractsComparisonTotals = models.JSONField(null=True)
    detailedContractsCostsComparisonPlot = models.JSONField(null=True)

    def __str__(self):
        return f"Recommendation for Consumer Unit {self.consumer_unit_id}"

    def to_dict(self):
        return {
            "consumer_unit": self.consumer_unit.id if self.consumer_unit else None,
            "currentContract": self.currentContract.id if self.currentContract else None,
            "generatedOn": self.generatedOn.isoformat() if self.generatedOn else None,
            "energyBillsCount": self.energyBillsCount,
            "currentTotalCost": self.currentTotalCost,
            "shouldRenewContract": self.shouldRenewContract,
            "nominalSavingsPercentage": self.nominalSavingsPercentage,
            "dates": [date.isoformat() for date in self.dates] if self.dates else None,
            "errors": self.errors,
            "warnings": self.warnings,
            "tariffStartDate": self.tariffStartDate.isoformat() if self.tariffStartDate else None,
            "tariffEndDate": self.tariffEndDate.isoformat() if self.tariffEndDate else None,
            "costsComparisonPlot": self.costsComparisonPlot,
            "recommendedContract": self.recommendedContract,
            "currentContractCostsPlot": self.currentContractCostsPlot,
            "contractsComparisonTotals": self.contractsComparisonTotals,
            "detailedContractsCostsComparisonPlot": self.detailedContractsCostsComparisonPlot,
        }
