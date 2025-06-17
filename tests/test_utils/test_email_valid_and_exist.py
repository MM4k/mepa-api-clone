import pytest

from utils.email.valid_email import verify_email_is_valid


def test_email_exist_and_valid():
    assert verify_email_is_valid("lucaslopesfrazao2003@gmail.com") is True


def test_email_invalid_format():
    with pytest.raises(Exception):
        verify_email_is_valid("invalid-email")
    with pytest.raises(Exception):
        verify_email_is_valid("invalid@.com")
    with pytest.raises(Exception):
        verify_email_is_valid("invalid@com")
    with pytest.raises(Exception):
        verify_email_is_valid("email@nonexistentdomain12345.com")
    with pytest.raises(Exception):
        verify_email_is_valid("example@domainwithoutmx.com")

    def test_email_valid_but_nonexistent():
        with pytest.raises(Exception):
            verify_email_is_valid("nonexistentemail@example.com")

    def test_email_with_special_characters():
        with pytest.raises(Exception):
            verify_email_is_valid("special@char!email.com")
        with pytest.raises(Exception):
            verify_email_is_valid("special@char#email.com")

    def test_email_with_subdomain():
        assert verify_email_is_valid("user@mail.example.com") is True

    def test_email_with_long_domain():
        assert verify_email_is_valid("user@subdomain.example.co.uk") is True
