from django.contrib import admin

# username is Jon
# password is cobb1234

# Register your models here.
from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping
# from orders.models import Order, MenuItem, OrderDetail, ItemOrderDetail, Category, PizzaTopping, CheesesteakTopping

admin.site.register(Order)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(OrderDetail)
admin.site.register(PizzaTopping)
admin.site.register(CheesesteakTopping)
