# Generated by Django 5.1.7 on 2025-03-27 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0016_alter_contract_off_peak_contracted_demand_in_kw_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='subgroup',
            field=models.CharField(blank=True, choices=[('A1', '≥ 230 kV'), ('A2', 'de 88 kV a 138 kV'), ('A3', 'de 69 kV'), ('A3a', 'de 30 kV a 44 kV'), ('A4', 'de 2,3 kV a 25 kV'), ('AS', '< a 2,3 kV, a partir de sistema subterrâneo de distribuição')], max_length=3, null=True),
        ),
    ]
