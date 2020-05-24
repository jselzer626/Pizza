from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping
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
    fields = ['order', 'item', 'quantity', 'toppings']
    category = ''

    def get_initial(self):
        itemId = self.request.GET.get('item', '')
        itemOrdered = MenuItem.objects.filter(pk=itemId).first()
        return {'item': itemOrdered}

    # this provides the item category so the view can be filtered based on what details need to be provided
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itemId = self.request.GET.get('item', '')
        context['category'] = MenuItem.objects.filter(pk=itemId).first().category
        return context
