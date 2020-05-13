from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="users/")
def index(request):
    return render(request, "orders/menu.html")
