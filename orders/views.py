from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping
from django.views.generic import ListView
from django.views.generic.edit import CreateView
# Create your views here.
@login_required(login_url="users/")
def index(request):
    return render(request, "orders/userhome.html")

def loadMenu(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, "orders/create.html", context)

class addGeneralItem(CreateView):
    model = OrderDetail
    fields = ['order', 'item', 'quantity', 'toppings', 'notes', 'sandwichToppings', 'extraCheese', 'size']

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
        except Order.DoesNotExist:
            currentOrder = None
        return OrderDetail.objects.filter(order = currentOrder)
