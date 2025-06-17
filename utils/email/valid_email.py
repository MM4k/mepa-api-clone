from email_validator import EmailNotValidError, validate_email


def verify_email_is_valid(email):
    try:
        validate_email(email, check_deliverability=True).normalized
    except EmailNotValidError as e:
        raise Exception(f"Email not valid: {e}")
    return True
