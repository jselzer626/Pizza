from django.urls import path

from . import views
from orders.views import addGeneralItem

# should be for a welcome page
urlpatterns = [
    path("", views.index, name="index"),
    path("loadMenu", views.loadMenu, name="loadMenu"),
    path("addGeneralItem", addGeneralItem.as_view(), name="addGeneralItem")
]
