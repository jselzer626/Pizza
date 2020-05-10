from django.db import models
from django.db.models import Sum

# Create your models here.
# this will be used as the base class for all menu items and as the main class for pasta and salads
class Category(models.Model):
    FOOD_CATEGORIES = [
        ('PST', 'Pasta'),
        ('PZA', 'Pizza'),
        ('SUB', 'Sandwiches'),
        ('PLT', 'Platters'),
        ('SLD', 'Salads')
    ]
    name = models.CharField(max_length=3, choices=FOOD_CATEGORIES)

    def __str__(self):
        return self.name

class PizzaTopping(models.Model):

    PIZZA_TOPPINGS = [
        ('Pepperoni','Pepperoni'),
        ('Sausage','Sausage'),
        ('Mushrooms','Mushrooms'),
        ('Onions','Onions'),
        ('Ham','Ham'),
        ('CanadianBacon', 'Canadian Bacon'),
        ('Pineapple','Pineapple'),
        ('Eggplant', 'Eggplant'),
        ('TomatoBasil', 'Tomato & Basil'),
        ('GreenPeppers', 'Green Peppers'),
        ('Hamburger', 'Hamburger'),
        ('Spinach', 'Spinach'),
        ('Artichoke', 'Artichoke'),
        ('BuffaloChicken', 'Buffalo Chicken'),
        ('BarbecueChicken', 'Barbecue Chicken'),
        ('Anchovies', 'Anchovies'),
        ('BlackOlives', 'Black Olives'),
        ('FreshGarlic', 'Fresh Garlic'),
        ('Zucchini', 'Zucchini')
    ]
    name=models.CharField(max_length=20, choices=PIZZA_TOPPINGS)

    def __str__(self):
        return f"{self.name}"

class CheesesteakTopping(models.Model):

    CHEESESTEAK_TOPPING = [
        ('MSH', 'Mushrooms'),
        ('GPP', 'Green Peppers'),
        ('ONS', 'Onions')
    ]
    name=models.CharField(max_length=3, choices=CHEESESTEAK_TOPPING)

    def __str__(self):
        return f"{self.name}"

class MenuItem(models.Model):

    #would need a foreign key for the order with which its associated
    name = models.CharField(max_length=30)
    priceSmall = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    priceLarge = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    PIZZA_STYLES = [
        ('NML', "Normal"),
        ('SCL', "Sicilian")
    ]
    pizzaStyle = models.CharField(max_length=3, choices=PIZZA_STYLES, blank=True)
    pizzaToppingsCount = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.pizzaStyle}"

class Order(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(MenuItem, blank=True, through='ItemOrderDetail')
    completed = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Number: {self.id} "

    def updateTotal(self):
        for item in self.items.all():
            total += item.itemorderdetail_set.first().total

class ItemOrderDetail(models.Model):

    ITEM_SIZES = [
        ('SM', "Small"),
        ('LG', "Large")
    ]
    size = models.CharField(max_length=2, blank=True, choices=ITEM_SIZES)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    toppings = models.ManyToManyField(PizzaTopping, blank=True)
    sandwichToppings = models.ManyToManyField(CheesesteakTopping, blank=True)
    total = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    extraCheese = models.BooleanField(default=False)

    def update(self):
        # handle cheese
        cheeseFee = 0
        if self.extraCheese == True:
            cheeseFee = .50
        if self.size == '' or self.size == 'small':
            self.total = self.quantity * self.item.priceSmall + cheeseFee
        else:
            self.total = self.quantity * self.item.priceLarge + cheeseFee

    def __str__(self):
        if self.extraCheese == True:
            return f"{self.item} X {self.quantity} {self.toppings} +XTRA Cheese  @ {self.total}"
        else:
            return f"{self.item} X {self.quantity} {self.toppings} @ {self.total}"
