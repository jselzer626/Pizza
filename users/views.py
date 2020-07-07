from django import forms
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
    next = request.POST.get('next') if request.POST.get('next') != '' else "/"
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(next)
    else:
        return render(request, "users/login.html", {"message": "Invalid Credentials. Please try again or create a new account!"})

def register_confirm(request):
    username = request.POST["new_username"]
    try:
        User.objects.get(username=username)
        return render(request, "users/register.html", {"message": "Username already taken, please choose something different!"})
    except User.DoesNotExist:
        password = request.POST["new_password"]
        email = request.POST["email"]
        next = request.POST.get('next') if request.POST.get('next') != '' else "/"
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        login(request, user)
        return HttpResponseRedirect(next)

def logout_view(request):
    logout(request)
    return redirect("/")
