from django.db import models

# Create your models here.

# orders
class Order(models.Model):

    # can access total price by using aggregate with variable.items.aggregate(total_price=Sum('price')).total_price
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Number: {self.id}"

# this will be used as the main class for salads, pasta, platters -> pizza and subs will have a subclass for toppings
class Item(models.Model):

    #would need a foreign key for the order with which its associated
    name = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1, related_name="items")

    #item sizes
    NONE = "NA"
    SMALL = "SM"
    LARGE = "LG"
    SIZE_CHOICES = [
        (NONE, 'N/A'),
        (SMALL, 'Small'),
        (LARGE, 'Large')
    ]

    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default=NONE)

    def __str__(self):
        if self.size == 'NA':
            return f"{self.name} : {self.price}"
        else:
            return f"{self.name} {self.size}: {self.price}"

class Pizza(Item):
    # type
    NORMAL = "NML"
    SICILIAN = "SCL"
    PIZZA_TYPE_CHOICES = [
        (NORMAL, "Normal"),
        (SICILIAN, "Sicilian")
    ]

    type = models.CharField(max_length=3, choices=PIZZA_TYPE_CHOICES, default=NORMAL)

    toppings = models.CharField(max_length=73, default="Cheese")

    def __str__(self):
        return f"{self.name} {self.type} {self.size} {self.toppings}: {self.price}"
