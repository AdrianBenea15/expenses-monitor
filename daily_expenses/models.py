from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self, email, name, region, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")
        if not region:
            raise ValueError("Please choose a region!")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, region=region)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, region, password):
        """Create and save new superuser with details"""
        user = self.create_user(email, name, region, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    region_choices = (("Europe", "Europe"), ("Asia", "Asia"), ("America", "America"))
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=50, choices=region_choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'region']

    def get_full_name(self):
        """Retrieve fullname of the user"""
        return self.name

    def get_region(self):
        """Retrieve region of the user"""
        return self.region

    def __str__(self):
        """Return string representation of our user"""
        return self.email
