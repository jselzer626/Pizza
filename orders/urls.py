from django.urls import path

from . import views
from orders.views import addGeneralItem, viewCart, deleteItem, editItem, deleteOrder
from django.contrib.auth.decorators import login_required

# path("addGeneralItem/<int:pk>/", login_required(login_url="users/")(addGeneralItem.as_view()), name="addGeneralItem"


# should be for a welcome page
urlpatterns = [
    path("", views.index, name="index"),
    path("loadMenu", views.loadMenu, name="loadMenu"),
    path("addGeneralItem/<int:pk>/", addGeneralItem.as_view(), name="addGeneralItem"),
    path("editItem/<int:pk>/", editItem.as_view(), name="editItem"),
    path("viewCart", viewCart.as_view(), name="viewCart"),
    path("deleteItem/<int:pk>/", deleteItem.as_view(), name="deleteOrderItem"),
    path("manageOrders", views.manageOrders, name="manageOrders"),
    path("manageOrders/<str:msg>/", views.manageOrders, name="manageOrders"),
    path("deleteOrder/<int:pk>/", deleteOrder.as_view(), name="deleteOrder"),
    path("markOrderComplete/<int:pk>/", views.markOrderComplete, name="markOrderComplete"),
    path("showAboutPage", views.showAboutPage, name="showAboutPage"),
    path("checkOut/<int:pk>/<str:orderMethod>/", views.checkOut, name="checkOut")
]
