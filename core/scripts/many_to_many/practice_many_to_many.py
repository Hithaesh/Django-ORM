from core.models import Staff, Restaurant
from django.db import connection
from pprint import pprint

def run():
  # staff, created = Staff.objects.get_or_create(name="Luke")
  # print(staff, created)
  # print(type(staff.restaurants))
  # print(Staff.objects.all())

  ### Add ###
  """
  add() can add multiple entries at once, but they must be passed as separate arguments, not as a single QuerySet
  """
  # print(f"Before: {staff.restaurants.all()}")
  ### NOT POSSIBLE (when passing Queryset) ### 
  # staff.restaurants.add(Restaurant.objects.first())
  # print(f"After: {staff.restaurants.all()}")


  ### using UNPACKING ###
  # print(f"Before: {staff.restaurants.all()}")
  # staff.restaurants.add(*Restaurant.objects.all()[1:5]) # Unpacks the queryset
  # print(f"After: {staff.restaurants.all()}")

  ### Count ###
  # print(f"Before: {staff.restaurants.all()}")
  # print(staff.restaurants.count())
  # print(f"After: {staff.restaurants.all()}")

  ### Remove ###
  # staff.restaurants.remove(*Restaurant.objects.all()[:3])

  ### Clear ###
  # print(f"Before: {staff.restaurants.all()}")
  # print(staff.restaurants.clear())
  # print(f"After: {staff.restaurants.all()}")


  ## Set ### 
  # print(f"Before: {staff.restaurants.all()}")
  # staff.restaurants.set(Restaurant.objects.all()[:3])
  # print(f"After: {staff.restaurants.all()}")


 ### Q. Return only the Italian Restaurant Staffs? ###

  # italian_staffs = staff.restaurants.filter(restaurant_type = Restaurant.TypeChoices.ITALIAN)
  # print(italian_staffs)

  staffs = Staff.objects.prefetch_related("restaurants")

  
 

  pprint(connection.queries)


  # ### Remove ###
  # print(staff.restaurants.remove)