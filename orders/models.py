from django.db import models, IntegrityError
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse

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
        return self.get_name_display()

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
        return self.get_name_display()

class CheesesteakTopping(models.Model):

    CHEESESTEAK_TOPPING = [
        ('MSH', 'Mushrooms'),
        ('GPP', 'Green Peppers'),
        ('ONS', 'Onions')
    ]
    name=models.CharField(max_length=3, choices=CHEESESTEAK_TOPPING)

    def __str__(self):
        return self.get_name_display()

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
        if self.pizzaStyle != '':
            return f"{self.name} - ({self.get_pizzaStyle_display()})"
        else:
            return f"{self.name}"

class Order(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(MenuItem, blank=True, through='OrderDetail')
    completed = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def updateTotal(self):
        order_items = OrderDetail.objects.filter(order = self.id).all()
        self.total = order_items.aggregate(Sum('total'))['total__sum'] if len(order_items) > 0 else 0.0
        self.save()
        return self.total

    def __str__(self):
        return f"Order #{self.id} Total: {self.total}"

# this class will roll up to order and will contain the number and type of item being ordered. This will be the parent of Item Detail which holds individual details for each item ordered(i.e. size, toppings, etc.)
class OrderDetail(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ITEM_SIZES = [
    ('SM', "Small"),
    ('LG', "Large")
    ]
    size = models.CharField(max_length=2, blank=True, choices=ITEM_SIZES)
    quantity = models.IntegerField(default=1)
    toppings = models.ManyToManyField(PizzaTopping, blank=True)
    sandwichToppings = models.ManyToManyField(CheesesteakTopping, blank=True)
    extraCheese = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    notes = models.CharField(max_length=64, blank=True)

    def updateTotal(self):
        self.total = self.item.priceLarge * self.quantity if self.size == 'LG' else self.item.priceSmall * self.quantity
        self.save()
        return self.total

    def get_absolute_url(self):
        return reverse("loadMenu")

    def __str__(self):
        self.updateTotal()
        showToppings = True if self.toppings.all().count() > 0 or self.sandwichToppings.all().count() > 0 else False
        if self.item.category == 'PZA':
            item_pizza_toppings = [str(elem) for elem in self.toppings.all()]
            return f"{self.item} {item_pizza_toppings} X {self.quantity} - {self.total}" if showToppings else f"{self.item} No toppings X {self.quantity} - {self.total}"
        elif self.item.category == 'SUB':
            extraCheese = 'XTRA Cheese' if {self.extraCheese} else ''
            item_sandwich_toppings = [str(elem) for elem in self.sandwichToppings.all()]
            return f"{self.item} {item_sandwich_toppings} X {self.quantity} - {self.total}" if showToppings else f"{self.item} No toppings X {self.quantity} - {self.total}"
        else:
            return f"{self.item} {self.size} X {self.quantity} - {self.total}"
