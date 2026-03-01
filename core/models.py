from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from core.user_manager import UserManager

# Restuarant Model
# Rating Model
# Sale Model


def validate_restuarant_name_startswith_a(value):
  if not value.startswith('a'):
    raise ValidationError("restaurant name must start with char 'a'")

class Restaurant(models.Model):
  class TypeChoices(models.TextChoices):
    INDIAN = 'IN', 'Indian'
    CHINESE = 'CH', 'Chinese'
    ITALIAN = 'IT', 'Italian'
    GREEK = 'GR', 'GREEK'
    MEXICAN = 'MX', 'Mexican'
    FASTFOOD = 'FF', 'Fast Food'
    OTHER = 'OT', 'Other'

  name = models.CharField(max_length=100, validators=[validate_restuarant_name_startswith_a])
  website = models.URLField(default="")
  date_opened = models.DateField()
  longitude = models.FloatField()
  latitude = models.FloatField()
  restaurant_type = models.CharField(max_length=2, choices=TypeChoices.choices, default=TypeChoices.OTHER)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Restuarant Name: {self.name} | Restuarant Type: {self.restaurant_type}"


class Rating(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="ratings")
  rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Restaurant : {self.restaurant} | Rating : {self.rating}"


class Sale(models.Model):
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
  income = models.DecimalField(max_digits=8, decimal_places=2)
  datetime = models.DateTimeField()

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Restuarant: {self.restaurant} | Income: {self.income}"


class Staff(models.Model):
  name = models.CharField(max_length=255)
  restaurants = models.ManyToManyField(Restaurant)

  def __str__(self):
    return self.name
  
  
# class StaffRestaurant(models.Model):
#   staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#   restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
#   salary = models.DecimalField(max_digits=20, decimal_places=10, null=True)


class UserAccount(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)

  objects = UserManager()

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []

  def __str__(self):
    return f"Email: {self.email}"