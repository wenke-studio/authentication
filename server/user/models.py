from __future__ import annotations

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Manager(BaseUserManager):
    def _create_user(self, email: str, password: str | None, **extra_fields: dict) -> User:
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()  # user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: dict) -> User:
        # a superuser should have all permissions by default
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email: str, password: str | None = None, **extra_fields: dict) -> User:
        # a user should not be staff or superuser by default
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Main
    email = models.EmailField(unique=True, editable=False)
    password = models.CharField(max_length=255)

    # Meta
    username = models.CharField(max_length=255, default="")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = Manager()

    def __str__(self) -> str:
        return self.username or self.email
