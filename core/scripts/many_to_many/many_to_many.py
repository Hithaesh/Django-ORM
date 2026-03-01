import random
from django.db import connection
from core.models import *


def run():
  # staff, created = Staff.objects.get_or_create(name="Praveen")
  # print(staff, created)

  # print(staff.restaurants.all())
  """
  Add
  """
  # To add a restaurant to a staff:
  # 1. Staff Object should be present.
  # 2. Using the instance obj, can associate Restaurant object to it
  # 3. We have a Junction Table where Staff_pk and Restaurant_pk is stored

  # count = Restaurant.objects.count()
  # num = random.randint(0, count)
  # print(f"Count: {count}, Number: {num}")
  # print(type(staff.restaurants))

  # staff.restaurants.add(Restaurant.objects.first())
  # print(staff.restaurants.count())
  # staff.restaurants.add(Restaurant.objects.first())

  """
  Remove
  """
  #staff.restaurants.remove()
  # Specify which staff to remove also can be done
  # staff.restaurant.remove(
  # Restaurant.objects.first() or querset with slice
  #)

  """
  Count
  """
  # print(staff.restaurants.count())

  """
  SET
  """
  # staff.restaurants.set(Restaurant.objects.all()[:2])
  # print(staff.restaurants.count())

  """
  CLEAR
  """
  # staff.restaurants.clear()
  # print(staff.restaurants.count())

  """
  CREATE
  """


  """
  FILTER
  """

  # staff.restaurants.set(Restaurant.objects.all()[:10])


  # Return only the italian restaurant staffs
  # italian_staffs = staff.restaurants.filter(restaurant_type = Restaurant.TypeChoices.ITALIAN)
  # print(staff.restaurants.count())
  # print(italian_staffs)


  # Return the staffs of a restaurant
  # restaurant = Restaurant.objects.get(pk=69)

  # print(restaurant.staff_set.all())

  """
  add method
  """
  # restaurant.staff_set.add(staff)

  """
  REMOVE
  """
  # restaurant.staff_set.remove(Staff.objects.first())
  #print(restaurant.staff_set.all())

  """
  CLEAR
  """
  #restaurant.staff_set.clear()
  #print(restaurant.staff_set.all())

  """
  Q. Find all restaurants where a staff member makes more than 30k?
  """
  # Before we need to add staff with salary
  # print(staff.restaurants.count())
  # staff.restaurants.set(Restaurant.objects.all()[:10], through_defaults={'salary': random.randint(25_000, 80_000)})
  # print(staff.restaurants.count())

  # print(staff.staffrestaurant_set.filter(salary__gt = 10))


  #TODO: Create a Staff Member

  staff, created = Staff.objects.get_or_create(name="Hithaesh")
  print(staff)
  print(created)

  """
  ADD
  """
  # staff.restaurants.add(*Restaurant.objects.all()[:2])

  """
  REMOVE
  """
  restaurants = staff.restaurants.all()
  restaurant = random.choice(restaurants)
  print(restaurant)
  staff.restaurants.remove(restaurant)

  """
  SET
  """