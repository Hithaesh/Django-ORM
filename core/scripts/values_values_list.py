from datetime import timedelta
from pprint import pprint
from django.utils import timezone

from django.db import connection
from django.db.models.functions import Concat, Length, Upper
from django.db.models import CharField, Count, Max, Min, Sum, Prefetch, Avg, Value
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
  # restaurants = Restaurant.objects.values(name_upper=Upper('name'))
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

  # ratings_avg = Rating.objects.aggregate(avg=Avg('rating'))
  # print(ratings_avg['avg'])

  """
  Q. Average ratings of each restaurant
  """

  """
  Solution: 
  - use aggregate() when whole queryset result
  - use annotate() per-object result

  Here it is for each restaurant
  """
  ### This is giving the average rating of all the Restaurant model ###
  # restaurants = Restaurant.objects.aggregate(avg_rating=Avg('ratings_rating'))
  # print(restaurants)

  """
  Classic N + 1 query

    # for r in Restaurant.objects.all():
    #   rating = r.objects.aggregate(avg=Avg('ratings__rating'))
    #   print(rating.get('avg')) 
  """

  # restaurants = Restaurant.objects.annotate(avg_rating = Avg('ratings__rating'))
  # print(restaurants[0])

  """
  Min() and Max()
  """

  # income_dict = Sale.objects.aggregate(
  #   min=Min('income'),
  #   max=Max('income'),
  #   avg=Avg('income'),
  #   count=Count('income')
  # )
  # print(income_dict)

  """
  Last month of the data
  """
  # last_month = timezone.now() - timedelta(days=31)

  # print(
  #   Sale.objects.filter(
  #   datetime__gte=last_month,
  #    ).aggregate(
  #     min=Min('income'),
  #     max=Max('income'),
  #     avg=Avg('income'),
  #     count=Count('income')
  #   )
  # )

  """
  ANNOTATE Models with .annotate method
  """
  # Fetch all restaurants, and let's assume we want to get the number of
  # characters in the name of the restaurant. So "sxy" = 3

  # restaurants = Restaurant.objects.annotate(
  #   len_name = Length('name')
  # )
  # print(restaurants.first().len_name)
  # print(restaurants.values("name", "len_name"))

  """
  Q. Filter restaurants name with more than 10 characters
  """
  # Using the annotate
  # restaurants = Restaurant.objects.annotate(
  #   len_name = Length('name')
  # ).filter(len_name__gt = 10).values('name', 'len_name')

  # print(restaurants)


  """
  .concat() method used to concatenate two or more fields from the DB
  """
  # Restaurant 1 [Rating: 4.3]

  # concatenation = Concat('name', Value(' [Rating: '), Avg('ratings__rating'), Value(']'),
  #   output_field=CharField()
  # )

  # restaurants = Restaurant.objects.annotate(
  #   message=concatenation
  # )

  # for r in restaurants:
  #   print(r.message)

  # NOTE: To display the field names that can be accessed from Restaurant model
  # fields = Restaurant._meta.get_fields()

  # for f in fields:
  #   print(f.name)

  """
  Q. Add a total_sales field to all the restaurants
  """
  # restaurants = Restaurant.objects.annotate(
  #   total_sales=Sum('sale__income')
  # )

  # print([r.total_sales for r in restaurants])

  """
  SQL: 
  SELECT r.*, SUM(s.income) as total_sales
  FROM restaurant as r
  LEFT OUTER JOIN
  sale as s 
  ON r.id = s.restaurant
  GROUP BY r.id

  Q. Find restaurnats whose total_sales > 1000
  SELECT r.*, SUM(s.income) as total_sales
  FROM restaurant as r
  LEFT JOIN 
  sale as s
  ON r.id = s.restaurant
  GROUP BY r.id
  HAVING total_sales > 1000
  """
  # restaurants = Restaurant.objects.annotate(
  #   total_sales=Sum('sale__income')
  # ).filter(total_sales__gt=1000)
  

  """
  Q. Annotate a field for number of ratings they recieved
  """

  # restaurants = Restaurant.objects.annotate(
  #   no_of_ratings=Count('ratings__rating')
  # ).values('name', 'no_of_ratings')

  # This is different
  # print(Restaurant.objects.values('name').annotate(no_of_ratings=Count('ratings')))

  """
  SQL
  SELECT r.name, COUNT(ra.rating) as no_of_ratings
  FROM restaurant r
  LEFT JOIN
  rating ra
  ON r.id = ra.restaurant
  GROUP BY r.name
  """

  """
  Q. Need average rating for all distinct restaurant types
  """
  # restaurants = Restaurant.objects.values(
  #   "restaurant_type"
  # ).annotate(
  #   avg_rating = Avg("ratings__rating")
  # ).distinct()

  """
  SQL:
  SELECT r.restaurant_type, AVG(ra.rating)
  FROM restaurant r
  LEFT JOIN
  rating ra
  ON r.id = ra.restaurant_id
  GROUP BY r.restaurant_type
  """


  """
  Q. Total number of sales for each restaurant
  """
  restaurant = Restaurant.objects.annotate(total_income = Sum("sale__income")) \
  .filter(total_sales__gt=1000)

  print(restaurant.values("name", "restaurant_type", "total_income"))

  """
  SQL:
  SELECT r.name, r.restaurant_type, SUM(s.income) as total_income
  FROM restaurant r
  LEFT JOIN
  sale s
  ON r.id = s.restaurant_id
  GROUP BY r.id, r.name, r.restaurant_type
  HAVING SUM(s.income) > 1000
  """

  # NOTE: Before Aggregation use WHERE, After Aggregation use HAVING
  """
  In SQL:
  - Non aggregated fields used in SELECT statements must be added to GROUP BY
  """

"""
BELOW IS THE CLASSIC EXAMPLE OF N + 1 Query
"""

# Executes 1 query to fetch distinct restaurant types
restaurant_types = Restaurant.objects.values_list('restaurant_type', flat=True).distinct()

# Loop runs N times
for type in restaurant_types:
    # Executes 1 query per iteration → N queries
    restaurants = Restaurant.objects.filter(
        restaurant_type=type
    ).annotate(avg_rating=Avg('ratings__rating'))

    for r in restaurants:
        print(f"{r.restaurant_type} restaurant avg rating: {r.avg_rating}")

# Total queries = 1 + N
pprint(connection.queries)
