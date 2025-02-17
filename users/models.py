from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Manager for the custom user model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The user must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given email and password.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of username.
    """

    ROLE_CHOICES = [
        ("employee", "Employee"),
        ("restaurant_admin", "Restaurant Admin"),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    objects = CustomUserManager()

    def __str__(self):
        """
        Returns a string representation of the user.
        """
        return f"{self.name} {self.surname} ({self.email})"
