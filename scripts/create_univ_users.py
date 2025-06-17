#!/usr/local/bin/python

from random import random
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from users.models import UniversityUser
from contracts.models import Contract
from universities.models import University, ConsumerUnit
from tariffs.models import Distributor, Tariff
from contracts.models import Contract, EnergyBill
from users.models import UniversityUser

# Fetch all University objects
universities = University.objects.all()

# Loop through each university
for university in universities:
    # Get the acronym attribute from the University object
    acronym = university.acronym

    # Create a UniversityUser object with the required attributes
    # admin_university_user = UniversityUser.objects.create(
    #     university=university,
    #     type=UniversityUser.university_admin_user_type,
    #     password='senha',  # Set the password to the university acronym
    #     email=f'usuario2@{acronym.lower()}.br',  # Construct the email
    #     first_name="João",
    #     last_name="da Silva",
    #     is_seed_user=True
    # )

    university_user = UniversityUser.objects.create(
        university=university,
        password='senha',
        email=f'usuario2@{acronym.lower()}.br',  # Construct the email
        first_name="Fulano",
        last_name="da Silva",
        is_seed_user=True
    )

    # Optionally, print out a message for each created user
    print(f'Created admin user for {university.name} with email: usuario2@{acronym.lower()}.br')