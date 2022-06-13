"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier for
    authentication instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        # require that an email must be present
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        # make sure the 2 lines below are as shown, Django uses these fields
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    # use email as unique identifier
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    # determines if user can login to django admin panel
    is_staff = models.BooleanField(default=False)

    # specify all objects of User are from the UserManager class
    objects = UserManager()

    # identify the field to be used to login as a user
    USERNAME_FIELD = 'email'
