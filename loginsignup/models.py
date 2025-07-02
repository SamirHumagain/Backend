from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# 1. Define your custom user manager here
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

# 2. Define your CustomUser model here
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('owner', 'Venue Owner'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')

    objects = CustomUserManager()  # Connect your custom manager here
