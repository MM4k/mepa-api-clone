import pytest

from users.models import UniversityUser


@pytest.fixture
def sysadmin(db):
    return UniversityUser.objects.create(
        type=UniversityUser.Type.SUPER_USER,
        first_name="Sys",
        last_name="Admin",
        email="sysadmin@admin.com",
        password="admin@12345",
    )


@pytest.fixture
def admin_a(db, university_a):
    return UniversityUser.objects.create(
        university=university_a,
        type=UniversityUser.Type.UNIVERSITY_ADMIN,
        first_name="Manager",
        last_name="User A",
        email="manager@university_a.com",
        password="manager@12345",
    )


@pytest.fixture
def admin_b(db, university_b):
    return UniversityUser.objects.create(
        university=university_b,
        type=UniversityUser.Type.UNIVERSITY_ADMIN,
        first_name="Manager",
        last_name="User B",
        email="manager@university_b.com",
        password="manager@12345",
    )


@pytest.fixture
def user_a(db, university_a):
    return UniversityUser.objects.create(
        university=university_a,
        type=UniversityUser.Type.UNIVERSITY_USER,
        first_name="Operational",
        last_name="User A",
        email="operational@university_a.com",
        password="operational@12345",
    )


@pytest.fixture
def user_b(db, university_b):
    return UniversityUser.objects.create(
        university=university_b,
        type=UniversityUser.Type.UNIVERSITY_USER,
        first_name="Operational",
        last_name="User B",
        email="operational@university_b.com",
        password="operational@12345",
    )


@pytest.fixture
def guest_a(db, university_a):
    return UniversityUser.objects.create(
        university=university_a,
        type=UniversityUser.Type.UNIVERSITY_GUEST,
        first_name="Guest",
        last_name="User",
        email="guest@unb.br",
    )


@pytest.fixture
def guest_b(db, university_b):
    return UniversityUser.objects.create(
        university=university_b,
        type=UniversityUser.Type.UNIVERSITY_GUEST,
        first_name="Guest",
        last_name="User",
        email="guest@unb.br",
    )
