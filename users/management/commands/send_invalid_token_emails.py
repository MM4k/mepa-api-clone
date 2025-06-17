from datetime import datetime

from django.core.management.base import BaseCommand

from users.authentications import Password
from users.models import CustomUser, UniversityUser, UserToken


class Command(BaseCommand):
    help = "Send email for all invalid trieds tokens"

    def handle(self, *args, **options) -> None:
        print("Envio de email para tokens inválidos está funcionando ||", datetime.now())

        users = UserToken.objects.get_user_users_waiting_to_send_email()

        for user in users:
            if user.account_password_status == "first_access":
                if isinstance(user, CustomUser) and not isinstance(user, UniversityUser):
                    user = UniversityUser.objects.get(id=user.id)
                Password.send_email_first_access_password(user)
            elif user.account_password_status == "admin_reset":
                Password.send_email_reset_password_by_admin(user.email)
            elif user.account_password_status == "user_reset":
                Password.send_email_reset_password(user.email)
