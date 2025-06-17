import pytest

from django.conf import settings


@pytest.mark.order(1)
def test_var_secret_key_is_available():
    assert settings.SECRET_KEY is not None


@pytest.mark.order(1)
def test_var_debug_is_available():
    assert settings.DEBUG is not None


@pytest.mark.order(1)
def test_var_environment_is_available():
    assert settings.ENVIRONMENT is not None
    assert settings.ENVIRONMENT == "test"
