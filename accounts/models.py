from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from neuralwave.validators import validate_phone_number
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, phone number, and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, phone number, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    terms_accepted = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Broker(models.Model):
    name = models.CharField(max_length=100)
    broker_symbol = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    client_user_id = models.CharField(max_length=100, null=True, blank=True)
    client_password = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.TextField(null=True, blank=True)
    client_secret = models.TextField(null=True, blank=True)
    totp = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.TextField(max_length=200, null=True, blank=True)
    refresh_token = models.TextField(max_length=200, null=True, blank=True)
    session_id = models.TextField(null=True, blank=True)
    token_expiry = models.DateTimeField(null=True, blank=True)
    connected = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return f"{self.user.email} - {self.broker.name}"