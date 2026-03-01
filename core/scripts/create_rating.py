from django.contrib.auth.models import User
from core.models import Restaurant, Rating


def run():

  user = User.objects.first()
  restaurant = Restaurant.objects.first()

  rating = Rating(
    user = user,
    restuarant = restaurant,
    rating = 3
  )
  rating.save()