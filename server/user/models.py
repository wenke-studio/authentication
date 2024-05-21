from __future__ import annotations

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models


class Manager(UserManager):
    def _create_user(self, email: str, password: str | None, **extra_fields: dict) -> User:
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()  # user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: dict) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email: str, password: str | None = None, **extra_fields: dict) -> User:
        # a member should not access the admin site
        extra_fields["is_staff"] = False

        # a member should not have superuser permissions
        extra_fields["is_superuser"] = False

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # Main
    email = models.EmailField(unique=True, editable=False)
    password = models.CharField(max_length=255)

    # Meta
    username = models.CharField(max_length=255, default=True, null=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def __str__(self) -> str:
        return self.username or self.email
