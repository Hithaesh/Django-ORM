from django.utils import timezone

from django.db.models import F, Q, Exists, Max, Min, Prefetch, Subquery, OuterRef
from django.db import connection

from core.models import Restaurant, Sale


def run():

  """
  Q. Fetch Italian, and chinese restuarant sales
  """
  ### Normal way ###
   
  italian_and_chinese = [Restaurant.TypeChoices.ITALIAN, Restaurant.TypeChoices.CHINESE]

  # sales = Sale.objects.filter(
  #   restaurant__restaurant_type__in=italian_and_chinese
  # ).count()

  ### Using Subquery Object ###
  # restaurants = Restaurant.objects.filter(restaurant_type__in=italian_and_chinese)

  # sales = Sale.objects.filter(
  #   restaurant__in=Subquery(restaurants.values('pk'))
  # )


  """
  Q. Get the latest sale for each restaurant
  """
  # restaurants = Restaurant.objects.all()

  # # annotate each Restaurant with the income generated from its MOST RECENT Sale
  # sales = Sale.objects.filter(restaurant = OuterRef('pk')).order_by('-datetime')

  # # outer query
  # restaurants = restaurants.annotate(
  #   last_sale_income = Subquery(sales.values('income')[:1]),
  #   last_expenditure_income = Subquery(sales.values('expenditure')[:1]),
  #   profit = F('last_sale_income') - F('last_expenditure_income'),
  # )


  # restaurants = Restaurant.objects.annotate(
  #   last_sale = Subquery(
  #     Sale.objects.filter(
  #       restaurant = OuterRef('pk')
  #     ).order_by('-datetime').values('income')[:1]
  #   )
  # )

  # for r in restaurants:
  #   print(f"{r.pk} | {r.last_sale_income} | {r.las}")


  """
  Q. Filter restaurants that have any sales with income > 85
  """
  # sales = Sale.objects.filter(
  #   restaurant = OuterRef('pk'),
  #   income__gt = 85
  # )

  # restaurants = Restaurant.objects.annotate(
  #   is_income_gt_85 = Exists(sales)
  # )

  # for r in restaurants:
  #   print(f"{r.pk} | {r.is_income_gt_85}")



  """
  Q. All restaurants sales for the last 5 days
  """
  last_day_sale = Sale.objects.aggregate(Max('datetime'))['datetime__max']

  five_days_ago = last_day_sale - timezone.timedelta(days=5)

  sales = Sale.objects.filter(
    datetime__gt=five_days_ago
  )

  restaurants = Restaurant.objects.prefetch_related(
    Prefetch("sale_set", queryset=sales)
  )

  for r in restaurants:
    print(f"{r.name} | {r.name}")

    for sale in r.sale_set.all():
      print(sale.income)


  print(connection.queries)
