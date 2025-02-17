from django.db import models
from django.contrib.auth import get_user_model
from restaurants.models import Menu

User = get_user_model()


class Vote(models.Model):
    """
    Model representing a user's vote for a specific menu.
    Each user can vote only once per menu.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "menu")

    def __str__(self):
        return f"{self.user.email} voted for {self.menu.restaurant.name} on {self.menu.date}"
