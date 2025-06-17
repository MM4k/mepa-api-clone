import pytest

from users import models
from utils.user.user_type_util import UserType


def test_get_user_type():
    with pytest.raises(Exception, match=r"User type \(\w+\) does not exist"):
        UserType.get_user_type("some_user_type")


def test_raise_exeception_for_invalid_user_type():
    # CT1
    invalid_user_type = "invalid"

    try:
        UserType.is_valid_user_type(invalid_user_type)
        assert False
    except Exception:
        assert True


def test_return_user_type_when_user_type_is_valid():
    # CT2
    user_type = models.CustomUser.all_user_types[0]
    assert user_type == UserType.is_valid_user_type(user_type)


def test_return_user_type_for_university_user_and_valid_university_user_type():
    # CT3
    user_model = models.UniversityUser
    user_type = models.CustomUser.university_user_types[0]
    assert user_type == UserType.is_valid_user_type(user_type, user_model)


def test_raise_expection_for_valid_university_user_and_invalid_university_user_type():
    # CT4
    user_model = models.UniversityUser
    user_type = "invalid"

    try:
        UserType.is_valid_user_type(user_type, user_model)
        assert False
    except Exception:
        assert True


def test_raise_exeception_for_invalid_university_user_and_valid_university_user_type():
    # CT5
    user_model = "invalid"
    user_type = models.CustomUser.university_user_types[0]

    try:
        UserType.is_valid_user_type(user_type, user_model)
        assert False
    except Exception:
        assert True


def test_return_user_type_for_custom_user_and_use_type_super_user():
    # CT6
    user = models.CustomUser
    user_type = models.CustomUser.super_user_type
    assert user_type == UserType.is_valid_user_type(user_type, user)


def test_raise_expection_for_valid_custom_user_and_not_super_user_type():
    # CT7
    user_model = models.CustomUser
    user_type = models.CustomUser.university_user_types[0]

    try:
        UserType.is_valid_user_type(user_type, user_model)
        assert False
    except Exception:
        assert True


def test_raise_exception_for_invalid_custom_user_and_valid_super_user_type():
    # CT8
    user_model = "invalid"
    user_type = models.CustomUser.university_user_types[0]

    try:
        UserType.is_valid_user_type(user_type, user_model)
        assert False
    except Exception:
        assert True


# Novos Casos de Teste para Cobertura MC/DC do método is_valid_user_type


def test_invalid_user_type_not_in_all_user_types():
    # CT1 (MC/DC)
    user_type = "invalid_user_type"
    with pytest.raises(Exception, match=r"User type \(\w+\) does not exist"):
        UserType.is_valid_user_type(user_type)


def test_valid_user_type_in_all_user_types():
    # CT2 (MC/DC)
    user_type = models.CustomUser.all_user_types[0]
    assert UserType.is_valid_user_type(user_type) == user_type


def test_user_type_in_university_user_types():
    # CT3 (MC/DC)
    user_type = models.CustomUser.university_user_types[0]
    user_model = models.UniversityUser
    assert UserType.is_valid_user_type(user_type, user_model) == user_type


def test_user_type_is_super_user_type():
    # CT6 (MC/DC)
    user_type = models.CustomUser.super_user_type
    user_model = models.CustomUser
    assert UserType.is_valid_user_type(user_type, user_model) == user_type
