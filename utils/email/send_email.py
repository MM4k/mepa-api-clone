from django.conf import settings
from django.core.mail import send_mail

from .templates_email import password_templates_email
from .valid_email import verify_email_is_valid


def send_email_first_access_password(user_name, university_name, recipient_email, link_to_reset_password_page):
    title, text_body = password_templates_email.template_email_first_access(
        user_name, university_name, link_to_reset_password_page
    )
    verify_email_is_valid(recipient_email)
    send_email(recipient_email, title, text_body)


def send_email_reset_password(user_name, recipient_email, link_to_reset_password_page):
    title, text_body = password_templates_email.template_email_recovery_password(
        user_name, link_to_reset_password_page
    )
    verify_email_is_valid(recipient_email)
    send_email(recipient_email, title, text_body)


def send_email_reset_password_by_admin(user_name, recipient_email, link_to_reset_password_page):
    title, text_body = password_templates_email.template_email_recovery_password_by_admin(
        user_name, link_to_reset_password_page
    )
    verify_email_is_valid(recipient_email)
    send_email(recipient_email, title, text_body)


def send_email(recipient_email: str, title: str, text_body: str):
    try:
        send_mail(
            subject=title,
            message="",  # Deixe a mensagem vazia, pois o conteúdo será HTML
            from_email=settings.EMAIL_HOST_USER or "no-reply@meusite.com",
            recipient_list=[recipient_email],
            fail_silently=False,
            html_message=text_body,  # Corpo do email em HTML
        )
    except Exception as error:
        raise Exception(f"Error sending email: {str(error)}")
