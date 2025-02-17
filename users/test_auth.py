import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

BASE_URL = "/api/auth/"


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_user():
    """
    Fixture to create a user for testing.
    """

    def _create_user(email, password="testpass123", role="employee"):
        return User.objects.create_user(email=email, password=password, role=role)

    return _create_user


@pytest.mark.django_db
def test_register_restaurant_admin(client):
    """
    Test registering a restaurant admin user.
    """
    payload = {
        "email": "admin@example.com",
        "name": "John",
        "surname": "Doe",
        "password": "password123",
        "role": "restaurant_admin",
    }
    response = client.post(f"{BASE_URL}register/", payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == payload["email"]
    assert response.data["role"] == "restaurant_admin"


@pytest.mark.django_db
def test_register_employee(client):
    """
    Test registering an employee user.
    """
    payload = {
        "email": "employee@example.com",
        "name": "Jane",
        "surname": "Smith",
        "password": "password123",
        "role": "employee",
    }
    response = client.post(f"{BASE_URL}register/", payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == payload["email"]
    assert response.data["role"] == "employee"


@pytest.mark.django_db
def test_register_with_invalid_data(client):
    """
    Test registration with invalid data (missing email or weak password).
    """
    payload = {
        "email": "",
        "name": "Invalid",
        "surname": "User",
        "password": "123",
        "role": "employee",
    }
    response = client.post(f"{BASE_URL}register/", payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_register_with_existing_email(client, create_user):
    """
    Test registration with an already existing email.
    """
    create_user(email="existing@example.com")
    payload = {
        "email": "existing@example.com",
        "name": "New",
        "surname": "User",
        "password": "password123",
        "role": "employee",
    }
    response = client.post(f"{BASE_URL}register/", payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_login_restaurant_admin(client, create_user):
    """
    Test logging in as a restaurant admin.
    """
    user = create_user(email="admin@example.com", role="restaurant_admin")
    payload = {"email": user.email, "password": "testpass123"}
    response = client.post(f"{BASE_URL}login/", payload)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_employee(client, create_user):
    """
    Test logging in as an employee.
    """
    user = create_user(email="employee@example.com", role="employee")
    payload = {"email": user.email, "password": "testpass123"}
    response = client.post(f"{BASE_URL}login/", payload)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_with_wrong_password(client, create_user):
    """
    Test login with an incorrect password.
    """
    user = create_user(email="user@example.com")
    payload = {"email": user.email, "password": "wrongpass"}
    response = client.post(f"{BASE_URL}login/", payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_login_non_existent_user(client):
    """
    Test login with a non-existent email.
    """
    payload = {"email": "notfound@example.com", "password": "password123"}
    response = client.post(f"{BASE_URL}login/", payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_logout(client, create_user):
    """
    Test logout (blacklisting the refresh token).
    """
    user = create_user(email="user@example.com")
    login_response = client.post(
        f"{BASE_URL}login/", {"email": user.email, "password": "testpass123"}
    )
    refresh_token = login_response.data["refresh"]

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}')
    response = client.post(f"{BASE_URL}logout/", {"refresh": refresh_token})
    assert response.status_code == status.HTTP_205_RESET_CONTENT


@pytest.mark.django_db
def test_logout_without_refresh(client, create_user):
    """
    Test logout without providing the refresh token.
    """
    user = create_user(email="user@example.com")
    login_response = client.post(
        f"{BASE_URL}login/", {"email": user.email, "password": "testpass123"}
    )

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {login_response.data["access"]}')
    response = client.post(f"{BASE_URL}logout/", {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_profile(client, create_user):
    """
    Test retrieving the profile of an authenticated user.
    """
    user = create_user(email="user@example.com")
    client.force_authenticate(user=user)
    response = client.get(f"{BASE_URL}profile/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
