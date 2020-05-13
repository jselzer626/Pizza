from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "orders/menu.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        context = {
            "user": request.user
        }
        return render(request, "orders/menu.html", context)
    else:
        return render(request, "users/login.html", {"message": "Invalid Credentials"})

def register_view(request):
    username = request.POST["new_username"]
    password = request.POST["new_password"]
    user = Users.objects.create_user(username=username, password=password)
    user.save()
    login(request, user)
    context = {
        "user": request.user
    }
    return render(request, "orders/menu.html", context)

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})
