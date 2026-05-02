
from django.db import connection
from django.db.models import F, Q, Sum
from pprint import pprint
from django.db.models.functions import Coalesce
from django.utils import timezone

from core.models import Restaurant, Sale


def run():
  """
  Q. Get all Italian or Mexican Restaurants
  """
  # it = Restaurant.TypeChoices.ITALIAN
  # mex = Restaurant.TypeChoices.MEXICAN

  # restaurants = Restaurant.objects.filter(
  # Q(restaurant_type=it) | Q(restaurant_type=mex)
  # )
  
  # print(restaurants)

  """
  Q. Find any restaurants that have the number "1" in the name
  """
  # restaurants = Restaurant.objects.filter(
  #   # name__contains = "1" # case-sensitive lookup
  #   name__icontains = "1" # case-insensitive lookup
  # )
  # print(restaurants)

  """
  Q. Restaurant name contains either the word "Italian" or the word "Mexican"
  """
  # restaurant = Restaurant.objects.filter(
  #   Q(name__icontains="italian") | Q(name__icontains="mexican")
  # )

  # it_or_mex = Q(name__icontains="italian") | Q(name__icontains="mexican")
  # recently_opened = Q(date_opened__gt=timezone.now() - timezone.timedelta(days=40))

  # restaurants = Restaurant.objects.filter(
  #   it_or_mex |
  #   recently_opened
  # )

  """
  NOT operator (~)
  """
  it_or_mex = Q(name__icontains="italian") | Q(name__icontains="mexican")
  not_recently_opened = Q(date_opened__gt=timezone.now() - timezone.timedelta(days=40))
  """
  Return the restaurants neither italian nor mexican
  """
  """
  SQL:
  SELECT *
  FROM Restaurant
  where name NOT LIKE "%italian% 
  AND name NOT LIKE %mexican%
  AND date_opened > '2025-03-07'
  """
  # restaurants = Restaurant.objects.filter(
  #   ~it_or_mex &
  #   ~not_recently_opened
  # )


  """
  Q. We want to find all Sales where:
  - profit is greater than expenditure
  - restaurant name contains a number

  SQL:
  SELECT s.*, r.*
  FROM Sale as s
  INNER JOIN
  Restaurant as r
  ON s.restaurant_id = r.id
  WHERE s.income > s.expenditure
  AND r.name ~ '[0-9]+'
  """

  # ----- First Approach ------
  # sales = Sale.objects.annotate(
  #   profit = F("income__gt")=0
  # ).filter(
  #   profit__gt=F("expenditure"),
  #   name__icontains__in=["0", "1", "2,", "3", "4", "5"]
  # )

  # ----- Optimised Approach -----
  res_with_name = Q(restaurant__name__regex=r"[0-9]+")
  profited = Q(income__gt=F("expenditure"))

  sales = Sale.objects.select_related("restaurant").filter(res_with_name & profited)
  print(sales)




  """
  Q. Find Restaurants where total profits > expenditure
  - grouping by Restaurant
  - aggregation sales/profits
  - comparing totals
  """

  """
  SQL: SELECT r.id, SUM(s.income) - SUM(s.expenditure) AS profit
  FROM Restaurant as r
  INNER JOIN
  Sale as s
  ON r.id = s.restaurant_id
  GROUP BY r.id
  HAVING SUM(s.income) - SUM(s.expenditure) > 0;
  """

  # NOTE: annotate() = GROUP BY happens automatically
  # NOTE: Internally does GROUP BY restaurant.id

  """
  WHERE  → filters rows (before grouping)
  HAVING → filters groups (after aggregation)
  """

  # restaurants = Restaurant.objects.annotate(
  #   profit = Sum("sale__income") - Sum("sale__expenditure")
  # ).filter(profit__gt=0)

  # # Better approach to prevent NULL values causing issues with calculation
  # restaurants = Restaurant.objects.annotate(
  #   total_income=Coalesce(Sum("sale__income"), 0),
  #   total_expenditure=Coalesce(Sum("sale__expenditure"), 0)
  # ).annotate(
  #   profit = F("total_income") - F("total_expenditure")
  # ).filter(
  #   profit__gt = 0
  # )

  # print(restaurants)
  pprint(connection.queries)