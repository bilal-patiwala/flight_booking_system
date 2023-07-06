from django.db import models
from django.contrib.auth.models import AbstractUser, User, AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_superuser(self, email, username,name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username,name, password, **other_fields)

    def create_user(self, email, username, name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254,unique=True)
    username = models.CharField(max_length=54, unique=True)
    name = models.CharField(max_length=54)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_flight_user = models.BooleanField(default=False)
    is_flight_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','name']


class Flight(models.Model):
    origin_country = models.CharField(max_length=50)
    origin_city = models.CharField(max_length=50)
    destination_country = models.CharField(max_length=50)
    destination_city = models.CharField(max_length=50)
    departure_time = models.TimeField(auto_now=False, auto_now_add=False)
    departure_date = models.DateField(auto_now=False, auto_now_add=False)
    total_seats_left = models.IntegerField(default=60)
    price = models.IntegerField()
    def __str__(self):
        return f"{self.origin_country} to {self.destination_country}"

class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=60)
    price = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} - Flight: {self.flight}, Passenger: {self.passenger}"