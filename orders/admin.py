from django.contrib import admin

# username is Jon
# password is cobb1234

# Register your models here.
from .models import Order, Item, Pizza

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Pizza)
