import pytest
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APIClient
from restaurants.models import Menu, Restaurant
from votes.models import Vote
from users.models import CustomUser

BASE_URL = "/api/votes/"


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def create_user(db):
    """Creates a user with a unique email."""

    def _create_user(email=None, password="testpass123", role="employee"):
        if email is None:
            email = f"user{CustomUser.objects.count()}@example.com"
        return CustomUser.objects.create_user(email=email, password=password, role=role)

    return _create_user


@pytest.fixture
def create_restaurant(db, create_user):
    """Creates a restaurant with a unique name and owner."""

    def _create_restaurant():
        name = f"Restaurant {Restaurant.objects.count()}"
        owner_email = f"owner{Restaurant.objects.count()}@example.com"
        owner = create_user(email=owner_email, role="restaurant_admin")
        return Restaurant.objects.create(name=name, owner=owner)

    return _create_restaurant


@pytest.fixture
def create_menu(db, create_restaurant):
    """Creates a menu for voting."""

    def _create_menu():
        restaurant = create_restaurant()
        return Menu.objects.create(
            restaurant=restaurant,
            date=now().date(),
            items={"Burger": 12, "Salad": 6, f"Dish{Menu.objects.count()}": 15},
        )

    return _create_menu


@pytest.fixture
def authorized_client(client, create_user, create_restaurant):
    """Returns an authenticated client with an employee user."""
    user = create_user()
    restaurant = create_restaurant()
    restaurant.employees.add(user)
    client.force_authenticate(user=user)
    return client, restaurant, user


@pytest.mark.django_db
def test_vote_for_menu(authorized_client, create_menu):
    """Test that a user can vote for a menu."""
    client, restaurant, user = authorized_client
    menu = create_menu()

    response = client.post(f"{BASE_URL}vote/", {"menu": menu.id}, format="json")

    assert (
        response.status_code == status.HTTP_201_CREATED
    ), f"🚨 Response: {response.data}"
    assert Vote.objects.filter(user=user, menu=menu).exists()


@pytest.mark.django_db
def test_cannot_vote_twice(authorized_client, create_menu):
    """Test that a user cannot vote for the same menu twice."""
    client, restaurant, user = authorized_client
    menu = create_menu()

    client.post(f"{BASE_URL}vote/", {"menu": menu.id}, format="json")
    response = client.post(f"{BASE_URL}vote/", {"menu": menu.id}, format="json")

    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    ), f"🚨 Response: {response.data}"
    assert Vote.objects.filter(user=user, menu=menu).count() == 1


@pytest.mark.django_db
def test_get_voting_results(authorized_client, create_menu):
    """Test retrieving the voting results."""
    client, restaurant, user = authorized_client
    menu = create_menu()

    client.post(f"{BASE_URL}vote/", {"menu": menu.id}, format="json")
    response = client.get(f"{BASE_URL}results/")

    assert response.status_code == status.HTTP_200_OK, f"🚨 Response: {response.data}"
    assert len(response.data) > 0
    assert any(
        result.get("menu_id") == menu.id and result.get("votes") == 1
        for result in response.data
    )
