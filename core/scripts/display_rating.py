from core.models import Rating
from django.db import connection
from pprint import pprint

def run():
  # print(Rating.objects.all())

  """
  Filter method
  """
  # print(Rating.objects.filter(rating__gte = 3))

  """
  Exclude method
  """
  # print(Rating.objects.exclude(rating__lt = 3))


  """
  Update method
  """
  rating = Rating.objects.first()
  rating.rating = 5
  rating.save()


  pprint(connection.queries)
