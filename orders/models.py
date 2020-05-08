from django.db import models
from django.db.models import Sum

# Create your models here.

# orders

# this will be used as the main class for salads, pasta, platters -> pizza and subs will have a subclass for toppings
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
        if self.size:
            return f"{self.name} @ ${self.price}"
        else:
            return f"{self.name} {self.size} @ {self.price}"

class Order(models.Model):

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(GeneralMenuItem, blank=True, through='ItemOrderDetail')
    completed = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Number: {self.id}"

    def updateTotal(self):
        for item in self.items.all():
            print(item)
            for detail in item.itemorderdetail_set.all():
                print(detail.total)
                self.total += detail.total

class ItemOrderDetail(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(GeneralMenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def update(self):
        self.total = self.quantity * self.item.price

    def __str__(self):
        return f"{self.order} X {self.quantity} : ${self.total}"
