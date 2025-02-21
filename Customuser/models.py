import uuid
from datetime import datetime, timedelta

from django.utils import timezone

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.


class Roles(models.Model):
    name = models.CharField(max_length=50)


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, default="abc@123")
    is_verified = models.BooleanField(default=False)
    roles = models.ManyToManyField(Roles)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

    def generate_auth_token(self, expiration=600):
        token = RefreshToken.for_user(self).access_token

        return str(token)


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('user', 'token'),)

    def is_valid(self):
        if self.expires < timezone.now() or not self.is_active:
            return False
        return True

# ForiegnKey: 1:M
# manytomany: M:M
# OneToOne: 1:1
# ManyToOne: M:1
