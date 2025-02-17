from rest_framework import serializers
from .models import Restaurant, Menu
from users.models import CustomUser


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for the Restaurant model.
    """

    owner = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role="restaurant_admin")
    )

    class Meta:
        model = Restaurant
        fields = ["id", "name", "owner", "employees", "created_at"]
        read_only_fields = ["id", "created_at"]


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for the Menu model.
    """

    class Meta:
        model = Menu
        fields = ["id", "restaurant", "date", "items"]


class AddEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for adding an employee to a restaurant.
    """

    employee_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Restaurant
        fields = ["id", "name", "employees", "employee_id"]
        read_only_fields = ["id", "name", "employees"]

    def validate(self, data):
        """
        Validate employee existence and permissions.
        """
        employee = CustomUser.objects.filter(
            id=data.get("employee_id"), role="employee"
        ).first()

        if not employee:
            raise serializers.ValidationError(
                {"error": "Invalid employee ID or user is not an employee."}
            )

        if employee in self.instance.employees.all():
            raise serializers.ValidationError({"error": "Employee is already added."})

        data["employee"] = employee
        return data

    def update(self, instance, validated_data):
        """
        Add the validated employee to the restaurant.
        """
        instance.employees.add(validated_data["employee"])
        return instance
