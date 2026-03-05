import random

from core.models import Staff, Restaurant, StaffRestaurant
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
  """ ### NOT POSSIBLE (when passing Queryset) ### """
  # staff.restaurants.add(Restaurant.objects.first())
  # print(f"After: {staff.restaurants.all()}")


  """ ### using UNPACKING ### """
  # print(f"Before: {staff.restaurants.all()}")
  # staff.restaurants.add(*Restaurant.objects.all()[1:5]) # Unpacks the queryset
  # print(f"After: {staff.restaurants.all()}")


  """ ### Count ### """
  # print(f"Before: {staff.restaurants.all()}")
  # print(staff.restaurants.count())
  # print(f"After: {staff.restaurants.all()}")


  """ ### Remove ### """
  # staff.restaurants.remove(*Restaurant.objects.all()[:3])


  """ ### Clear ### """
  # print(f"Before: {staff.restaurants.all()}")
  # print(staff.restaurants.clear())
  # print(f"After: {staff.restaurants.all()}")


  """ ### Set ### """
  # print(f"Before: {staff.restaurants.all()}")
  # staff.restaurants.set(Restaurant.objects.all()[:3])
  # print(f"After: {staff.restaurants.all()}")


  """ ### Q. Return only the Italian Restaurant Staffs? ### """
  # staff,created = Staff.objects.get_or_create(name="Hithaesh")

  # print(f"Staff object(instance): {staff}")

  # staff.restaurants.add(*Restaurant.objects.filter(
  #   restaurant_type=Restaurant.TypeChoices.ITALIAN)[:4]
  # )

  # italian_staffs = Restaurant.objects.prefetch_related("staff_set").filter(
  #   restaurant_type=Restaurant.TypeChoices.ITALIAN
  # )

  # print(italian_staffs)

  """### Simplest way ### """
  # italian_staff = staff.restaurants.filter(restaurant_type = Restaurant.TypeChoices.ITALIAN).first()

  # print(f"Italian Staff: {italian_staff.__dict__}")

  """### From Restaurant model, if we want to know the staffs working in this restaurant ###"""
  # restaurants = Restaurant.objects.all()
  # for r in restaurants:
  #   print(r.staff_set.all())



  """
  After adding an Extra Field to Many-to-Many relationship table
  """
  ### There are two ways we can associate salary to staff member, and with restaurant

  staff,created = Staff.objects.get_or_create(name="Hithaesh")
  restaurant_1 = Restaurant.objects.first()
  # restaurant_2 = Restaurant.objects.last()

  """
  First option
  """
  # StaffRestaurant.objects.create(
  #   staff=staff,
  #   restaurant=restaurant_1,
  #   salary=28_000
  # )

  # StaffRestaurant.objects.create(
  #   staff=staff,
  #   restaurant=restaurant_2,
  #   salary=26_000
  # )

  """
  Second option, where we can use the model manager methods like (add, clear, remove, and set)
  """
  staff.restaurants.clear()
  staff.restaurants.add(restaurant_1, through_defaults={"salary": 18_000})

  staff.restaurants.set(Restaurant.objects.all()[:10], through_defaults={"salary": random.randint(20_000, 80_000)})

  """
  Using prefetch_related with StaffRestaurant model
  
  jobs = StaffRestaurant.objects.prefetch_related("staff", "restaurant").all()

  for job in jobs:
    print(job.staff.name)
    print(job.restaurant.name)

  Step 1 — Fetch StaffRestaurant rows
  Step 2 -- Staff.objects.get(id=job.staff_id)
  Step 3 -- stores it in cache
  Step 4 -- uses the cached data to display the name

  This is N+1 query problem
  This help in mitigating N + 1 queries
  How?

  if prefetch_related is used, the workflow:
  1. Fetch all the staffrestaurant ids
  2. Query  — fetch all related Staff at once
  3. Django builds in-memory maps
  """

  pprint(connection.queries)

  # ### Remove ###
  # print(staff.restaurants.remove)