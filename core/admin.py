from django.contrib import admin
from core.models import Restaurant, Sale, Rating, UserAccount, Order, Product

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Sale)
admin.site.register(Rating)
admin.site.register(UserAccount)
admin.site.register(Order)
admin.site.register(Product)