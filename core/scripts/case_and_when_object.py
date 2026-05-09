from django.utils import timezone
import itertools
from pprint import pprint
from django.db import connection

from core.models import Restaurant, Sale
from django.db.models import F, Avg, BooleanField, Case, CharField, Count, Max, Min, Sum, Value, When

from django.db.models.functions import Coalesce

def run():
  """
  If-else statement in database level we use Case(), When() and then()
  

  ORM Syntax:
  Case
    When (expression is True, then = True),
    default = False,
    output_field = BooleanField()

  SQL Syntax:
  When
  """

  """
  SQL:
  SELECT r.*,
      CASE
        WHEN r.restaurant_type = 'italian' THEN True
        ELSE False
      END = True;
  FROM restaurant as r
  CASE
    WHEN r.restaurant_type = 'italian' THEN True
    ELSE False
  END = True;

  """
  # italian = Restaurant.TypeChoices.ITALIAN

  # restaurants = Restaurant.objects.annotate(
  #   is_italian = Case(
  #     When(restaurant_type = italian, then=True),
  #     default=False,
  #     output_field=BooleanField()
  #   )
  # )

  # print(
  #   restaurants.filter(is_italian=True)
  # )

  """
  Q. Have a new field indicates that a restaurant had 8 sales
  """
  # restaurants = Restaurant.objects.annotate(
  #   no_of_sales = Count('sale')
  # ).annotate(
  #   is_popular = Case(
  #     When(no_of_sales__gte = 8, then=True),
  #     default=False,
  #     output_field=BooleanField()
  #   )
  # )

  # print(
  #   restaurants.values("no_of_sales", "no_of_sales")
  # )

  """
  Q. 
  - Restaurant average rating > 3.5
  - Restaurant has more than 1 rating
  """

  # First Approach
  # restaurants = Restaurant.objects.annotate(
  #   avg_rating = Coalesce(Avg("ratings"), 0.0),
  #   ratings_count = Coalesce(Count("ratings"), 0)
  # ).annotate(
  #   has_valid_avg= Case(
  #     When(avg_rating__gt= 3.5, then=True),
  #     default=False,
  #     output_field=BooleanField()
  #   ),
  #   has_valid_ratings = Case(
  #     When(ratings_count__gt=1, then=True),
  #     default=False,
  #     output_field=BooleanField()
  #   )
  # )

  # Optimsed Approached
  # restaurants = Restaurant.objects.annotate(
  #   avg = Coalesce(Avg("ratings__rating"), 0.0),
  #   num_ratings = Count("ratings__pk")
  # ).annotate(
  #   ratingss = Case(
  #     When(avg__gt = 3.5, num_ratings__gt = 1, then=Value("Highly rated")),
  #     default=Value("Low Rated")
  #   )
  # )

  # print(
  #   restaurants.values("ratingss")
  # )


  """
  Q. Aggregating total Sales over each 10 day period,
    starting from the first sale up until the last.

    # 1th - 10th
    # 11th - 20th
  """

  first_sale = Sale.objects.aggregate(first_sale_date=Min("datetime"))["first_sale_date"]
  last_sale = Sale.objects.aggregate(last_sale_date=Max("datetime"))["last_sale_date"]

  print(f"First Sale: {first_sale}")
  print(f"Last Sale: {last_sale}")

  # generate a list of dates, each 10 days apart
  dates = []
  count = itertools.count()

  while(dt:= first_sale + timezone.timedelta(days=10*next(count))) <= last_sale:
    dates.append(dt)

  # Created When objects
  whens = [
    When(datetime__range = (dt, dt+timezone.timedelta(days=10)), then=Value(dt.date()))
    for dt in dates
  ]

  # Created Case objects
  case = Case(
    *whens, 
    output_field=CharField()
  )

  sales = Sale.objects.annotate(
    daterange = case
  ).values("daterange").annotate(
    total_income = Sum("income")
  )

  pprint(connection.queries)