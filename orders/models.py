from django.db import models
from django.db.models import Sum

size = models.CharField(max_length=1, blank=True, choices=ITEM_SIZES)

# Create your models here.
# this will be used as the base class for all menu items and as the main class for pasta and salads
class GeneralMenuItem(models.Model):

    #would need a foreign key for the order with which its associated
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    ITEM_SIZES = [
        ('S', "Small"),
        ('L', "Large")
    ]
    size = models.CharField(max_length=1, blank=True, choices=ITEM_SIZES)

    def __str__(self):
        return f"{self.name}"

class Platter(GeneralMenuItem):

    def __str__(self):
        return f"{self.name} {self.size}"

class Pizza(GeneralMenuItem):

    PIZZA_STYLES = [
        ('NML', "Normal"),
        ('SCL', "Sicilian")
    ]
    style = models.charField(max_length=3, choices=PIZZA_STYLES)
    toppings = models.ManyToManyField(PizzaTopping, blank=True)

    def __str__(self):
        return f"{self.name} {self.style} {self.toppings}"

class PizzaTopping(models.Model):

    TOPPINGS = [
        ('Pepperoni','Pepperoni')
        ('Sausage','Sausage')
        ('Mushrooms','Mushrooms')
        ('Onions','Onions')
        ('Ham','Ham')
        ('CanadianBacon', 'Canadian Bacon')
        ('Pineapple','Pineapple')
        ('Eggplant', 'Eggplant')
        ('TomatoBasil', 'Tomato & Basil')
        ('GreenPeppers', 'Green Peppers')
        ('Hamburger', 'Hamburger')
        ('Spinach', 'Spinach')
        ('Artichoke', 'Artichoke')
        ('BuffaloChicken', 'Buffalo Chicken')
        ('BarbecueChicken', 'Barbecue Chicken')
        ('Anchovies', 'Anchovies')
        ('BlackOlives', 'Black Olives')
        ('FreshGarlic', 'Fresh Garlic')
        ('Zucchini', 'Zucchini')
    ]
    name=models.charField(max_length=20, choices=TOPPINGS)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(GeneralMenuItem, blank=True, through='ItemOrderDetail')
    completed = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Number: {self.id} "

    def updateTotal(self):
        for item in self.items.all():
            total += item.itemorderdetail_set.first().total

class ItemOrderDetail(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(GeneralMenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def update(self):
        self.total = self.quantity * self.item.price

    def __str__(self):
        return f"{self.order} X {self.quantity} : ${self.total}"
