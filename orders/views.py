from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping

# Create your views here.
@login_required(login_url="users/")
def index(request):
    return render(request, "orders/userhome.html")

def createNewOrder(request):
    context = {
        'categories': Category.objects.all(),
        'menuItems': MenuItem.objects.all()
    }
    return render(request, "orders/create.html", context)
