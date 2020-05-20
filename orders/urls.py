from django.urls import path

from . import views

# should be for a welcome page
urlpatterns = [
    path("", views.index, name="index"),
    path("createNewOrder", views.createNewOrder, name="createNewOrder")
]
