from django.db import connection
from django.db.models.functions import Upper
from django.db.models import Count, Sum, Prefetch, Avg
from core.models import *

def run():
  """
  .values = Returns the queryset in the dict format and futhermore does group_by if fields are mentioned.
  SELECT (The columns you need you specify) right what is what .values() does and aggregation as well. 
  """

  """
  1. We want to fetch only the NAME, and DATE OPENED field from Restaurant model
  """
  # restaurants = Restaurant.objects.values('name', 'date_opened')[:5]
  # print(restaurants)
  """
  Output: <QuerySet [{'name': 'Pizzeria 1', 'date_opened': datetime.date(2026, 1, 5)}, {'name': 'Pizzeria 2', 'date_opened': datetime.date(2025, 12, 29)}, {'name': 'Golden Dragon', 'date_opened': datetime.date(2026, 1, 10)}, {'name': 'Bombay Bustle', 'date_opened': datetime.date(2025, 12, 12)}, {'name': 'McDonalds', 'date_opened': datetime.date(2025, 12, 5)}]>
  """

  """
  2. Transforming or aggregation values in DB level
  """
  # restaurants = Restaurant.objects.values(name_upper = Upper('name'))
  # print(restaurants)
  """
  Output: <QuerySet [{'name_upper': 'PIZZERIA 1'},]>
  SQL QUERY: [{'sql': 'SELECT UPPER("core_restaurant"."name") AS "name_upper" FROM "core_restaurant" LIMIT 21', 'time': '0.001'}]
  """

  """
  3. Getting related F.K values using values
  """

  # IT = Restaurant.TypeChoices.ITALIAN
  # restaurants = Rating.objects.filter(
  #   restaurant__restaurant_type = IT
  # ).values('rating', 'restaurant__name')
  # print(restaurants)


  # CH = Restaurant.TypeChoices.CHINESE
  # ratings = Rating.objects.filter(restaurant__restaurant_type=CH).values('rating', 'restaurant__name')
  # print(ratings)
  """
  Output: <QuerySet [{'rating': 2, 'restaurant__name': 'Pizzeria 1'},]>

  SQL Query:[{'sql': 'SELECT "core_rating"."rating" AS "rating", "core_restaurant"."name" AS "restaurant__name" FROM "core_rating" INNER JOIN "core_restaurant" ON ("core_rating"."restaurant_id" = "core_restaurant"."id") WHERE "core_restaurant"."restaurant_type" = \'IT\' LIMIT 21', 'time': '0.003'}]
  """

  """
  4. Getting related values using prefetch_related()
  This does LEFT OUTER JOIN
  """

  # ratings = Prefetch(
  #   "ratings",
  #   Rating.objects.filter(rating__gte = 3)
  # )

  # restaurants = Restaurant.objects.prefetch_related(ratings).values("name", "ratings__rating")
  # print(restaurants)

  """
  4. values_list = return the Queryset in tuples with only values, not key:value
  """
  # restaurants = Restaurant.objects.values_list('name')
  """
  Output: <QuerySet [('Pizzeria 1',), ('Pizzeria 2',), ('Golden Dragon',), ('Bombay Bustle',), ('McDonalds',), ('Taco Bell',), ('Chinese 2',), ('Chinese 3',), ('Indian 2',), ('Mexican 1',), ('Mexican 2',), ('Pizzeria 3',), ('Pizzeria 4',), ('Italian 1',)]>
  """


  """
  Use (flat = True) when you want to use only single field
  Flatten the Queryset with values in a list
  """
  # restaurants = Restaurant.objects.values_list('name', flat=True)
  # print(restaurants)
  """
  Output: <QuerySet ['Pizzeria 1', 'Pizzeria 2', 'Golden Dragon', 'Bombay Bustle', 'McDonalds', 'Taco Bell', 'Chinese 2', 'Chinese 3', 'Indian 2', 'Mexican 1', 'Mexican 2', 'Pizzeria 3', 'Pizzeria 4', 'Italian 1']>

  SQL: [{'sql': 'SELECT "core_restaurant"."name" AS "name" FROM "core_restaurant" LIMIT 21', 'time': '0.001'}]
  """

  """
  5. Aggregation and Annotation

  Aggregation is grouping
  """
  # Q. Count the number of rows in the Restaurant table
  # print(Restaurant.objects.filter(name__startswith='c').count())
  """
  Output: 2
  SQL: [{'sql': 'SELECT COUNT(*) AS "__count" FROM "core_restaurant" WHERE "core_restaurant"."name" LIKE \'c%\' ESCAPE \'\\\'', 'time': '0.002'}]
  """

  # Using Aggregate method returns a DICT
  # NOTE: Cannot chain multiple aggregation 
  
  # print(Restaurant.objects.aggregate(total=Count('id')))
  """
  Output:{'id__count': 2} , {'total': 14}

  SQL:[{'sql': 'SELECT COUNT("core_restaurant"."id") AS "id__count" FROM "core_restaurant" WHERE "core_restaurant"."name" LIKE \'c%\' ESCAPE \'\\\'', 'time': '0.001'}]
  """

  ratings_avg = Rating.objects.aggregate(avg=Avg('rating'))
  print(ratings_avg['avg'])

  print(connection.queries)