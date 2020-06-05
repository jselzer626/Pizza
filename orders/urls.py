from django.urls import path

from . import views
from orders.views import addGeneralItem, viewCart, deleteItem, editItem
from django.contrib.auth.decorators import login_required

# should be for a welcome page
urlpatterns = [
    path("", views.index, name="index"),
    path("loadMenu", views.loadMenu, name="loadMenu"),
    path("addGeneralItem/<int:pk>/", login_required(login_url="users/")(addGeneralItem.as_view()), name="addGeneralItem"),
    path("editItem/<int:pk>/", editItem.as_view(), name="editItem"),
    path("viewCart", viewCart.as_view(), name="viewCart"),
    path("deleteItem/<int:pk>/", deleteItem.as_view(), name="deleteOrderItem")
]
