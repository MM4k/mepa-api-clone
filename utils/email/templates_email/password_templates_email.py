from django.conf import settings


def template_email_first_access(user_name, university_acronym, link_reset_password_page):
    title = "Cadastrado na MEPA - Monitoramento de Energia em Plataforma Aberta"

    message = f"""
        == Esta é uma mensagem automática, não é necessário responder ==

        <p>Olá {user_name},</p>

        <p>Seu cadastrado foi criado na <a href="{settings.MEPA_FRONT_END_URL}">MEPA - Monitoramento de Energia em Plataforma Aberta</a> para análise do contrato de fornecimento de energia da(o) {university_acronym}.</p>

        Para acessar o sistema, cadastre uma senha clicando no link abaixo:<br>
        <a href="{link_reset_password_page}">{link_reset_password_page}</a>

        <p>Se nem você, nem a sua chefia imediata solicitaram o cadastro, você pode responder esta mensagem e pedir o cancelamento.</p>

        <p>Tenha um bom dia.</p>

        == Esta é uma mensagem automática, não é necessário responder ==
    """  # noqa

    return (title, message)


def template_email_recovery_password(user_name, link_reset_password_page):
    title = "Redefinição de senha -> MEPA - Monitoramento de Energia em Plataforma Aberta"

    message = f"""
        == Esta é uma mensagem automática, não é necessário responder ==

        <p>Olá {user_name},</p>

        <p>Você solicitou a redefinição da sua senha de acesso à <a href="{settings.MEPA_FRONT_END_URL}">MEPA - Monitoramento de Energia em Plataforma Aberta</a>.</p>

        Para criar uma nova senha, clique no link abaixo:<br>
        <a href="{link_reset_password_page}">{link_reset_password_page}</a>

        <p>Se você não solicitou a redefinição da senha, ignore esta mensagem.</p>

        <p>Tenha um bom dia.</p>

        == Esta é uma mensagem automática, não é necessário responder ==
    """  # noqa

    return (title, message)


def template_email_recovery_password_by_admin(user_name, link_reset_password_page):
    title = "Redefinição de senha -> MEPA - Monitoramento de Energia em Plataforma Aberta"

    message = f"""
        == Esta é uma mensagem automática, não é necessário responder ==

        <p>Olá {user_name},</p>

        <p>A redefinição da sua senha de acesso à <a href="{settings.MEPA_FRONT_END_URL}">MEPA - Monitoramento de Energia em Plataforma Aberta</a> foi realizada pela administração da plataforma. Sua senha atual foi desativada.</p>

        Para criar uma nova senha, clique no link abaixo:<br>
        <a href="{link_reset_password_page}">{link_reset_password_page}</a>

        <p>Tenha um bom dia.</p>

        == Esta é uma mensagem automática, não é necessário responder ==
    """  # noqa

    return (title, message)
