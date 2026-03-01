from django.db import connection
from core.models import Restaurant
from pprint import pprint

def run():
  """
  Get the sales for this restuarant
  """

  restaurant = Restaurant.objects.last()
  print(restaurant)
  sales = restaurant.sale_set.all()
  pprint(sales)

  print(connection.queries)
