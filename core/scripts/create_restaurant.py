from core.models import Restaurant
from django.utils import timezone
from django.db import connection

def run():
  
  # Instantiate the Model
  restaurant = Restaurant()
  restaurant.name = 'My Italian Restuarant'
  restaurant.latitude = 49.2
  restaurant.longitude = 50.2
  restaurant.date_opened = timezone.now()
  restaurant.restaurant_type = Restaurant.TypeChoices.ITALIAN

  restaurant.full_clean()
  restaurant.save()
  
  print(connection.queries)