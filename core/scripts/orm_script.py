from core.models import Rating, Restaurant
from pprint import pprint
from django.db import connection
from django.contrib.auth.models import User

def run():

  """
  Filter using the "filter" method, filter out all chinese restuarants
  """
  # filtered_restaurants = Restaurant.objects.filter(
  #   restaurant_type = Restaurant.TypeChoices.CHINESE,
  # )

  """
  Add Multiple filter conditions like condition-1 and condition-2
  Get restaurants which starts with the character 'a'
  """
  # filtered_restaurants_with_C = Restaurant.objects.filter(
  #   restaurant_type = Restaurant.TypeChoices.CHINESE,
  #   name__startswith = 'C'
  # )

  "-----------------------------------------------------------------------------------------------------------"
  """
  Filter queryset using "in" method
  """
  # pprint(Restaurant.TypeChoices.choices)
  # pprint(Restaurant.TypeChoices.labels)
  # pprint(Restaurant.TypeChoices.names)
  # pprint(Restaurant.TypeChoices.values)
  # pprint(Restaurant.TypeChoices.__members__)
  chinese = Restaurant.TypeChoices.CHINESE
  indian = Restaurant.TypeChoices.INDIAN
  italian = Restaurant.TypeChoices.ITALIAN
  check_types = [chinese, indian, italian]
  # filtered_restaurants_in_chinese_indian_italian = Restaurant.objects.filter(restaurant_type__in=check_types)
  # pprint(filtered_restaurants_in_chinese_indian_italian[0].__dict__)
  # pprint(filtered_restaurants_in_chinese_indian_italian[1].__dict__)
  # pprint(filtered_restaurants_in_chinese_indian_italian[-2].__dict__)
  # pprint(filtered_restaurants_in_chinese_indian_italian[-1].__dict__)

  "-----------------------------------------------------------------------------------------------------------"

  """
  Filter queryset using "exclude" method
  Which is inverse of "filter" method
  """
  exclude = {
    "restaurant_type": Restaurant.TypeChoices.CHINESE
  }
  # print(Restaurant.TypeChoices.CHINESE)
  # all_restuarants_count = Restaurant.objects.count()
  # restaurants_except_chinese = Restaurant.objects.exclude(**exclude)
  # print(f"All restaurant's Count: {all_restuarants_count}")
  # print(f"All restaurants except CHINESE count: {restaurants_except_chinese.count()}")
  # pprint(restaurants_except_chinese[0].__dict__)
  # pprint(restaurants_except_chinese)



  # Filter using Foreign Key valeus
  # restaurant = Restaurant.objects.last()
  # ratings = restaurant.ratings.all()
  # print("Rating", ratings)

  # ratings = Rating.objects.filter(restaurant__name__startswith='c')
  # print(ratings)

  '---------------------------------------------------------------------------------------'

  



  print("\nSQL Queries:")
  pprint(connection.queries)
