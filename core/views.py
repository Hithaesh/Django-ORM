from django.shortcuts import render
from django.db.models import Sum, Prefetch
from core.models import Restaurant, Sale, Rating, Staff
from django.db import connection
from django.utils import timezone
from pprint import pprint

# Create your views here.

def index(request):

  # restaurant = Restaurant.objects.all() 
  # print("Restaurants: ", restaurant)
  """
  N + 1, if we want to filter out their ratings for each restaurant.
  Solution: use prefetch_related (Reverse-relationship)
  - Basically it does seperate lookup for each relationship and does joining and stores it in queryset
  - Relationships: Many to Many, Many to One , GenericRelation (cannot be done using select_related) and GenericForeignKey
  """
  # restaurants = Restaurant.objects.prefetch_related('ratings', 'sale_set')
  # print(connection.queries)
  # To fetch each restaurants rating:
  # restaurants = Restaurant.objects.prefetch_related('ratings')
  # print(restaurants)
  # restaurant = Restaurant.objects.filter(name__istartswith='c').prefetch_related('ratings', 'sale_set')
  # restaurant = Restaurant.objects.prefetch_related('ratings', 'sale_set')


  """
  Get all 5-star ratings, and fetch all the sales for restaurants with 5-star ratings.
  """
  
  """
  N + 1, if we want to get all the ratings, of all the restaurant
  Solution: use select_related (for Foreign Keys[Many to One])
  - Does inner join with the parent table
  - select * from rating inner join restaurant on rating.id == restaurant.id where rating.id=5
  """

  # ratings = Rating.objects.filter(rating=5)
  # ratings = Rating.objects.filter(rating=5).select_related('restaurant')


  """
  TOPIC: Prefetch Objects

  Question: Get all 5-star ratings, and fetch all the sales for restaurants with 5-star ratings

  Solutions:

  Solution-1:
  - First query the restaurants with 5 star rating from RESTAURANT model using prefetch_related()
  - Annotate their total_income with the income field as we have pre-fetched related data.
  """
  """
  --- Method-1 --- 
  """
  # restaurants = Restaurant.objects.prefetch_related("ratings", "sale_set") \
  # .filter(ratings__rating=5) \
  # .annotate(total=Sum('sale_set__income'))

  #--- Method-2 ---
  """
  Get last 1 month sum of all the 5-star rating restaurants
  """

  # month_ago = timezone.now() - timezone.timedelta(days=30)
  # monthly_sales = Prefetch(
  #   'sale_set', # lookups
  #   queryset=Sale.objects.filter(datetime__gte = month_ago)
  # ) # creates a Prefetch object

  # rating = Prefetch(
  #   'ratings',
  #   queryset=Rating.objects.filter(rating=5)
  # )


  # restaurants = Restaurant.objects.prefetch_related("ratings", monthly_sales).filter(ratings__rating=5)
  restaurants = restaurants.annotate(total=Sum('sale__income'))

  ### PRACTICE QUESTIONS ###
  """
  Fetch all staff and list the names of restaurants they work at.
  """
  staffs = Staff.objects.prefetch_related("restaurants")

  """
  Fetch all restaurants and display:
  restaurant name
  type
  all staff names
  """
  # restaurants = 

  # print([r.total for r in restaurants])
  # context = {'ratings': ratings}
  context = {'restaurants': restaurants}
  return render(request, 'index.html', context)
