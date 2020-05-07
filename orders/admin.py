from django.contrib import admin

# username is Jon
# password is cobb1234

# Register your models here.
from .models import Order, GeneralMenuItem

admin.site.register(Order)
admin.site.register(GeneralMenuItem)
