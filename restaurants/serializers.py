from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Restaurant, Menu
from users.models import CustomUser


class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role="restaurant_admin")
    )

    class Meta:
        model = Restaurant
        fields = ["id", "name", "owner", "employees", "created_at"]

    def validate(self, data):
        """
        Validate that only restaurant admins can create a restaurant.
        """
        request = self.context["request"]
        if request.user.role != "restaurant_admin":
            raise serializers.ValidationError(
                "Only restaurant admins can create restaurants."
            )
        return data


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "restaurant", "date", "items"]

    def validate(self, data):
        request = self.context["request"]
        restaurant_id = self.context["view"].kwargs.get("restaurant_id")
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        if restaurant.owner != request.user:
            raise serializers.ValidationError(
                "Only the restaurant owner can create a menu."
            )

        data["restaurant"] = restaurant
        return data


class AddEmployeeSerializer(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Restaurant
        fields = ["id", "name", "employees", "employee_id"]
        read_only_fields = ["id", "name", "employees"]

    def validate(self, data):
        """
        Validate employee existence and permissions.
        """
        request = self.context["request"]
        restaurant = self.instance
        employee_id = data.get("employee_id")

        if restaurant.owner != request.user:
            raise serializers.ValidationError(
                {"error": "Only the restaurant owner can add employees."}
            )

        employee = CustomUser.objects.filter(id=employee_id, role="employee").first()
        if not employee:
            raise serializers.ValidationError(
                {"error": "Invalid employee ID or user is not an employee."}
            )

        if employee in restaurant.employees.all():
            raise serializers.ValidationError({"error": "Employee is already added."})

        data["employee"] = employee
        return data

    def update(self, instance, validated_data):
        """
        Add the validated employee to the restaurant.
        """
        employee = validated_data["employee"]
        instance.employees.add(employee)
        return instance
