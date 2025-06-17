import pytest

from rest_framework import status

from tests.fixtures import admin_a, guest_a, sysadmin, university_a, user_a
from universities.models import University


@pytest.mark.django_db
class TestUniversityViewSet:
    data = {
        "name": "Universidade Teste",
        "acronym": "UTEST",
        "cnpj": "42504316000160",
    }

    def test_sysadmin_can_create_university(self, sysadmin, client):
        client.force_authenticate(user=sysadmin)
        response = client.post("/api/universities/", self.data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_sysadmin_cannot_delete_university(self, sysadmin, client, university_a):
        client.force_authenticate(user=sysadmin)
        url = f"/api/universities/{university_a.id}/"
        response = client.delete(url)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_manager_cannot_create_university(self, admin_a, client):
        client.force_authenticate(user=admin_a)
        response = client.post("/api/universities/", self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_manager_cannot_delete_university(self, admin_a, client, university_a):
        client.force_authenticate(user=admin_a)
        response = client.delete(f"/api/universities/{university_a.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_create_university(self, user_a, client):
        client.force_authenticate(user=user_a)
        response = client.post("/api/universities/", self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_delete_university(self, user_a, client, university_a):
        client.force_authenticate(user=user_a)
        response = client.delete(f"/api/universities/{university_a.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_guest_cannot_create_university(self, guest_a, client):
        client.force_authenticate(user=guest_a)
        response = client.post("/api/universities/", self.data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_guest_cannot_delete_university(self, guest_a, client, university_a):
        client.force_authenticate(user=guest_a)
        response = client.delete(f"/api/universities/{university_a.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
