import pytest
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.test import APIClient
from rest_framework import status
from restaurants.models import Restaurant, Menu

User = get_user_model()

BASE_URL = "/api/restaurants/"


@pytest.fixture
def client():
    """Returns an API test client."""
    return APIClient()


@pytest.fixture
def create_user():
    """
    Fixture to create a user.
    """

    def _create_user(email, password="testpass123", role="restaurant_admin"):
        return User.objects.create_user(email=email, password=password, role=role)

    return _create_user


@pytest.fixture
def create_employee():
    """
    Fixture to create an employee user.
    """

    def _create_employee(email="employee@example.com", password="testpass123"):
        user = User.objects.create_user(email=email, password=password, role="employee")
        user.save()
        return user

    return _create_employee


@pytest.fixture
def create_restaurant(create_user):
    """
    Fixture to create a restaurant.
    """

    def _create_restaurant(name="Test Restaurant", owner_email="owner@example.com"):
        owner = create_user(email=owner_email, role="restaurant_admin")
        return Restaurant.objects.create(name=name, owner=owner)

    return _create_restaurant


@pytest.fixture
def create_menu(create_restaurant):
    """
    Fixture to create a menu item for a restaurant.
    """

    def _create_menu(restaurant, date=now().date(), items={"Pizza": 10, "Pasta": 8}):
        return Menu.objects.create(restaurant=restaurant, date=date, items=items)

    return _create_menu


@pytest.fixture
def authorized_client(client, create_restaurant):
    """
    Returns an authenticated client with a restaurant owner user.
    """
    restaurant = create_restaurant()
    client.force_authenticate(user=restaurant.owner)
    return client, restaurant


# -------------------------- RESTAURANT API TESTS --------------------------


@pytest.mark.django_db
def test_create_restaurant(authorized_client):
    """Test creating a new restaurant."""
    client, restaurant = authorized_client
    payload = {"name": "New Restaurant", "owner": restaurant.owner.id}

    response = client.post(BASE_URL, payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == payload["name"]


@pytest.mark.django_db
def test_update_restaurant(authorized_client):
    """Test updating a restaurant's details."""
    client, restaurant = authorized_client
    payload = {"name": "Updated Restaurant"}
    response = client.patch(f"{BASE_URL}{restaurant.id}/", payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Updated Restaurant"


@pytest.mark.django_db
def test_delete_restaurant(authorized_client):
    """Test deleting a restaurant."""
    client, restaurant = authorized_client
    response = client.delete(f"{BASE_URL}{restaurant.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Restaurant.objects.count() == 0


# -------------------------- EMPLOYEE MANAGEMENT TEST --------------------------


@pytest.mark.django_db
def test_add_employee_to_restaurant(authorized_client, create_employee):
    """Test adding an employee to a restaurant."""
    client, restaurant = authorized_client
    employee = create_employee()

    payload = {"employee_id": employee.id}
    response = client.patch(f"{BASE_URL}{restaurant.id}/add-employee/", payload)

    assert response.status_code == status.HTTP_200_OK
    assert employee in restaurant.employees.all()


@pytest.mark.django_db
def test_add_employee_invalid_email(authorized_client):
    """Test adding an employee with an invalid email."""
    client, restaurant = authorized_client

    payload = {"employee_id": 99999}  # Немає такого ID
    response = client.patch(f"{BASE_URL}{restaurant.id}/add-employee/", payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_add_employee_not_an_employee(authorized_client, create_user):
    """Test adding a user who is not an employee."""
    client, restaurant = authorized_client
    non_employee = create_user(email="admin@example.com", role="restaurant_admin")

    payload = {"employee_id": non_employee.id}
    response = client.patch(f"{BASE_URL}{restaurant.id}/add-employee/", payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# -------------------------- MENU API TESTS --------------------------


@pytest.mark.django_db
def test_create_menu(authorized_client):
    """Test creating a menu for a restaurant."""
    client, restaurant = authorized_client
    payload = {
        "restaurant": restaurant.id,
        "date": str(now().date()),
        "items": {"Burger": 12, "Salad": 6},
    }
    response = client.post(f"{BASE_URL}{restaurant.id}/menus/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_update_menu(authorized_client, create_menu):
    """Test updating a menu."""
    client, restaurant = authorized_client
    menu = create_menu(restaurant=restaurant)

    payload = {"items": {"Steak": 15, "Fries": 5}}

    response = client.patch(
        f"{BASE_URL}{restaurant.id}/menus/{menu.id}/", payload, format="json"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_menu(authorized_client, create_menu):
    """Test deleting a menu."""
    client, restaurant = authorized_client
    menu = create_menu(restaurant=restaurant)

    response = client.delete(f"{BASE_URL}{restaurant.id}/menus/{menu.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Menu.objects.count() == 0


# -------------------------- DAILY MENU TEST --------------------------


@pytest.mark.django_db
def test_get_current_day_menu(authorized_client, create_menu):
    """Test retrieving the menu for the current day."""
    client, restaurant = authorized_client
    create_menu(restaurant=restaurant)

    response = client.get(f"{BASE_URL}{restaurant.id}/daily-menu/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert "items" in response.data[0]
