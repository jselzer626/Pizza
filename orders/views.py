from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
import stripe
import json

# Create your views here.
@login_required(login_url="users/")
def index(request):
    return render(request, "orders/userhome.html")

def loadMenu(request):
    context = {
        'message': request.GET.get('message', ''),
        'categories': Category.objects.all()
    }
    return render(request, "orders/create.html", context)

class addGeneralItem(CreateView):
    model = OrderDetail
    fields = ['order', 'item', 'quantity', 'toppings', 'notes', 'sandwichToppings', 'extraCheese', 'size']
    success_url = "loadMenu?message=itemAdded"

    def get_initial(self):
        itemId = self.request.GET.get('item', '')
        itemOrdered = MenuItem.objects.filter(pk=itemId).first()
        try:
            currentOrder = Order.objects.get(user=self.request.user, completed=False)
        except Order.DoesNotExist:
            currentOrder = Order(user=self.request.user)
            currentOrder.save()
        return {'item': itemOrdered,
                'order': currentOrder}

    '''def form_valid(self, form):
        order = Order.objects.get(user=self.request.user, completed=False)
        print(f"Before: {order.total}")
        order.updateTotal()
        order.save()
        print(f"After: {order.total}")
        return super().form_valid(form)'''

    # this provides the item category so the view can be filtered based on what details need to be provided

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itemId = self.request.GET.get('item', '')
        cheeseSteak = True if MenuItem.objects.get(pk=itemId).name == "Steak + Cheese" else False
        context['category'] = MenuItem.objects.filter(pk=itemId).first().category
        context['cheesteak'] = cheeseSteak
        return context

class viewCart(ListView):

    template_name = "orders/viewCart.html"

    def get_queryset(self):
        try:
            currentOrder = Order.objects.get(user=self.request.user, completed=False)
            currentOrder.updateTotal
        except Order.DoesNotExist:
            currentOrder = None
        return OrderDetail.objects.filter(order = currentOrder)

class deleteItem(DeleteView):

    model = OrderDetail
    success_url = reverse_lazy('viewCart')
