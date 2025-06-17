#!/usr/local/bin/python

from users.models import UniversityUser

sysadmin = UniversityUser.objects.create(
    password='admin',
    email='sysadmin@admin.com',
    first_name='Sysadmin',
    last_name='adm',
    type=UniversityUser.Type.SUPER_USER,
    is_seed_user=True
)
