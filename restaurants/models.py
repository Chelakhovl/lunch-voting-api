from django.db import models
from django.conf import settings
from django.utils import timezone


class Restaurant(models.Model):
    """
    Represents a restaurant with an owner and employees.
    """

    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_restaurants",
    )
    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="employee_restaurants", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """
    Represents a menu for a specific restaurant on a given date.
    """

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    date = models.DateField(default=timezone.now)
    items = models.JSONField()  # Stores menu items as a list of dishes
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("restaurant", "date")

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"
