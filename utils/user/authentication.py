import random
import string

from django.conf import settings


def generate_random_password():
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))


def create_token_response(token, user_id, user_email, user_first_name, user_last_name, user_type):
    response = {
        "token": token,
        "user": {
            "id": user_id,
            "email": user_email,
            "firstName": user_first_name,
            "lastName": user_last_name,
            "type": user_type,
        },
    }

    return response


def create_valid_token_response(is_valid_token):
    return {"is_valid_token": is_valid_token}


def generate_link_to_reset_password(token, user_first_name, password_status):
    if password_status == "first_access":
        endpoint = settings.MEC_ENERGIA_PASSWORD_ENDPOINT_FIRST_ACCESS
    elif password_status == "admin_reset":
        endpoint = settings.MEC_ENERGIA_PASSWORD_ENDPOINT_ADMIN_RESET
    elif password_status == "user_reset":
        endpoint = settings.MEC_ENERGIA_PASSWORD_ENDPOINT_USER_RESET
    else:
        raise ValueError("Invalid password_status")

    endpoint_string = f"{settings.MEPA_FRONT_END_URL}/{endpoint}/"
    user_first_name = f"?nome={user_first_name}"
    token_string = f"&token={token}"
    return endpoint_string + user_first_name + token_string
