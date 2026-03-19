
from pprint import pprint
import random

from django.db import connection

from core.models import Rating, Sale
from django.db.models import F, Q, Count
from django.db.models.functions import Least


def run():
  """
  A F object represents the value of the model field.
  """

  # rating = Rating.objects.filter(rating=4).first()

  # print(f"Rating before: {rating.rating}")
  # rating.rating = F('rating') + 0.1
  # rating.save()

  #NOTE: Need to reload the object after saving it
  # rating.refresh_from_db()

  # print(f"Rating after: {rating.rating}")


  """
  Update existing rating with multiplying with 2
  Example:
  rating = 1, new_rating = 1 *2
  """
  # multiple = 2

  # rating = Rating.objects.update(
  #   rating = Least((F('rating') * multiple), 10)
  # )
  # print(rating)


  """
  """
  # sales = Sale.objects.filter(income__gt = 0, income__lte= 10)
  # print(f"SALES: {len(sales)}")
  
  # for sale in sales:
  #   sale.expenditure = random.uniform(5, 10)

  # Sale.objects.bulk_update(sales, ['expenditure'])


  # sales = Sale.objects.select_related('restaurant').filter(expenditure__gt = F("income"))
  # print(sales)

  """
  Annotate using F Expression()

  Add a field called profit (income - expenditure)
  """
  # sales = Sale.objects.annotate(
  #   profit = F("income") - F("expenditure")
  # ).order_by("-profit") # This is done in DB level

  # print(sales.first().profit)


  """
  Find the count of Profit, and loss
  """
  sales = Sale.objects.aggregate(
    profit=Count("id", filter=Q(income__gt=F("expenditure"))),
    loss=Count("id", filter=Q(income__lt=F("expenditure")))
  )

  print(sales) # {'profit': 54, 'loss': 46}


  # pprint(connection.queries)
