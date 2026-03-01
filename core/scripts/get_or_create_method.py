from django.db import connection
from django.utils import timezone
from core.models import Restaurant, Sale


def run():
  restuarant = Restaurant.objects.first()

  created_obj, status = Sale.objects.get_or_create(
    restuarant = restuarant, 
    income = 250.12,
  )
  
  print(created_obj)
  print(status)

  print(connection.queries)