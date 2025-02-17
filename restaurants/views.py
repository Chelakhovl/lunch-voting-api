from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer, AddEmployeeSerializer


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
    permission_classes = [permissions.IsAuthenticated]


class AddEmployeeView(generics.UpdateAPIView):
    """
    API for restaurant owners to add employees to their restaurant.
    """

    queryset = Restaurant.objects.all()
    serializer_class = AddEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Calls the serializer to validate and add an employee.
        """
        restaurant = self.get_object()
        serializer = self.get_serializer(
            instance=restaurant,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Employee added successfully."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuListCreateView(generics.ListCreateAPIView):
    """
    API for listing all menus of a restaurant and adding a new menu.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns all menus belonging to a specific restaurant.
        """
        restaurant_id = self.kwargs.get("restaurant_id")
        return Menu.objects.filter(restaurant_id=restaurant_id)


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API for retrieving, updating, or deleting a menu item.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]


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
