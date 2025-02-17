from django.urls import path
from .views import (
    RestaurantListCreateView,
    RestaurantDetailView,
    AddEmployeeView,
    MenuListCreateView,
    MenuDetailView,
    DailyMenuView,
)

urlpatterns = [
    path("", RestaurantListCreateView.as_view(), name="restaurant-list-create"),
    path("<int:pk>/", RestaurantDetailView.as_view(), name="restaurant-detail"),
    path("<int:pk>/add-employee/", AddEmployeeView.as_view(), name="add-employee"),
    path(
        "<int:restaurant_id>/menus/",
        MenuListCreateView.as_view(),
        name="menu-list-create",
    ),
    path(
        "<int:restaurant_id>/menus/<int:pk>/",
        MenuDetailView.as_view(),
        name="menu-detail",
    ),
    path("<int:restaurant_id>/daily-menu/", DailyMenuView.as_view(), name="daily-menu"),
]
