from core.models import Restaurant
from core.models import Rating
from pprint import pprint


def run():
  """
  Q. We want all the ratings for this restuarant
  """
  restaurant = Restaurant.objects.first()

  #ratings = restaurant.rating_set.all()
  ratings = restaurant.ratings.all()

  sales = restaurant.sales.all()

  print(sales)
  print(ratings)



