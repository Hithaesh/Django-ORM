from django.db import connection
from random import random

from django.db.models import F, Avg, Sum
from django.db.models.functions import Coalesce
from core.models import Rating, Restaurant
from pprint import pprint


def run():
  
  """
  isnull ORM method
  """
  # print(
  #   Restaurant.objects.filter(capacity__isnull=True)
  # )

  """
  Ordering with null values in Django with order by
  1. Null values comes first
  2. Non-null values comes last
  """
  # restaurant = Restaurant.objects.first()
  # restaurant2 = Restaurant.objects.last()

  # restaurant.capacity = 20
  # restaurant2.capacity = 21
  # restaurant.save()
  # restaurant2.save()
  # print(
  #   Restaurant.objects.order_by("capacity").values("capacity")
  # )

  """
  Q. Want the non-null values to be ordering first
  Solution: 
  - F()
  - nulls_first or nulls_last keyword argument
  - To Expression.asc() or desc() to control the field's null values 
  """

  # print( 
  #   Restaurant.objects.order_by(F("capacity").desc(nulls_last=True)).values("capacity")
  # )


  """
  Coalesce
  """
  # Restaurant.objects.update(capacity=None)
  # print(
  #   Restaurant.objects.aggregate(
  #     total_cap=Coalesce(Sum("capacity"), 0)
  #   )
  # )

  # Another use case (default to the existing)
  print(
    Restaurant.objects.annotate(
      name_value = Coalesce(F('nickname'), F("name"))
    ).values("name_value")
  )

  """
  Alternative way
  """
  # print(
  #   Rating.objects.filter(rating__lt=0).aggregate(total_avg=Avg("rating", default=0.0))
  # )

  pprint(connection.queries)