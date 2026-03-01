from core.models import Restaurant
from django.db import connection


def run():

  """
  all() method
  """
  # restaurants = Restaurant.objects.all()
  # print(restaurants) # Queryset (python like dict)

  """
  first() method
  """
  # restaurant = Restaurant.objects.first()
  # print(restaurant) # Model Instance

  """
  Indexing
  """
  # restaurant = Restaurant.objects.all()[0]
  # print(restaurant)
  

  print(connection.queries)