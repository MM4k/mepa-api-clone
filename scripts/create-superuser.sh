#!/bin/bash

create_script="
from users.models import CustomUser

password = 'admin'
email = 'admin@admin.com'
first_name = 'Admin'

CustomUser.objects.create_superuser(email=email, password=password, first_name=first_name, is_seed_user=True)
"

echo "$create_script" | ./manage.py shell

