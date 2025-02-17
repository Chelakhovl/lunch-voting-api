from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer, AddEmployeeSerializer
from services.permissions.is_restaurant_owner import IsRestaurantOwner
from services.permissions.is_menu_owner import IsMenuOwner


class RestaurantListCreateView(generics.ListCreateAPIView):
    """
    API for creating a restaurant and listing all restaurants.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for retrieving, updating, or deleting a restaurant.
    """

    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]


class AddEmployeeView(generics.UpdateAPIView):
    """
    API for restaurant owners to add employees to their restaurant.
    """

    queryset = Restaurant.objects.all()
    serializer_class = AddEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]


class MenuListCreateView(generics.ListCreateAPIView):
    """
    API for listing all menus of a restaurant and adding a new menu.
    """

    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsMenuOwner]

    def get_queryset(self):
        """
        Returns all menus belonging to a specific restaurant.
        """
        return Menu.objects.filter(restaurant_id=self.kwargs["restaurant_id"])


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for retrieving, updating, or deleting a menu item.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsMenuOwner]


class DailyMenuView(APIView):
    """
    API for retrieving the current day's menu for a specific restaurant.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, restaurant_id):
        """
        Fetch today's menu for the given restaurant.
        """
        today = now().date()
        menu = Menu.objects.filter(restaurant_id=restaurant_id, date=today)
        serializer = MenuSerializer(menu, many=True)
        return Response(serializer.data)
