from core.models import Restaurant, Sale
from django.utils import timezone

def run():

  sale = Sale(
    restuarant = Restaurant.objects.last(),
    income = 69.69,
    datetime = timezone.now()
  )
  sale.save()

  Sale.objects.create(
    restuarant = Restaurant.objects.first(),
    income = 2.35,
    datetime = timezone.now()
  )