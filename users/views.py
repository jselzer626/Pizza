from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return redirect("/")

def register(request):
    return render(request, "users/register.html")

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("/")
    else:
        return render(request, "users/login.html", {"message": "Invalid Credentials"})

def register_confirm(request):
    username = request.POST["new_username"]
    password = request.POST["new_password"]
    user = User.objects.create_user(username=username, password=password)
    user.save()
    login(request, user)
    return redirect("/")

def logout_view(request):
    logout(request)
    return redirect("/")
