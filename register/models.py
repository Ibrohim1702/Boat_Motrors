from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class ManagerUser(BaseUserManager):
    def create_user(self, email, password, is_active=True, is_superuser=False, is_staff=False, *args, **kwargs):
        user = self.model(
                          password=password,
                          email=email,
                          is_active=is_active,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        return self.create_user(email, password, is_superuser=True, is_staff=True, **kwargs)


class User(AbstractUser):
    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=12, null=True, blank=True)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    state = models.CharField(max_length=50)
    region = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    adres = models.CharField(max_length=128)
    status = models.BooleanField
    username = False

    data_joined = models.DateTimeField(editable=False, auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = ManagerUser()
    REQUIRED_FIELDS = ['first_name']

    def format(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.first_name,
            "is_staff": self.is_staff,
            "data_joined": self.data_joined,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
        }

    def __str__(self):
        return self.first_name
