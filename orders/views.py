from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.forms import ModelForm, Textarea
from django.contrib.auth.decorators import login_required
from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import StrictButton
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


class addItemForm(forms.ModelForm):

    class Meta:
        model = OrderDetail
        fields = ['order', 'item', 'quantity', 'toppings', 'notes', 'sandwichToppings', 'extraCheese', 'size']
        widgets = {
            'notes': Textarea(attrs={'cols':6, 'rows':3, 'placeholder': "Any special requests..."})
        }

    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.label_class = 'col-lg-4'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        'item',
        'quantity',
        'size',
        'toppings',
        'sandwichToppings',
        'extraCheese',
        'notes',
        ButtonHolder(
                Submit('submit', 'Add To Cart')
            )
    )

    # formatting certain labels
    def __init__(self, *args, **kwargs):
        super(addItemForm, self).__init__(*args, **kwargs)
        self.fields['sandwichToppings'].label = "Sandwich Toppings"
        self.fields['extraCheese'].label = 'Extra Cheese? (check for yes)'

class addGeneralItem(CreateView):
    model = OrderDetail
    form_class = addItemForm
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

    # update item total based on selections made in form
    def form_valid(self, form):
        form.instance.updateTotal()
        return super().form_valid(form)

    # this provides the item category so the view can be filtered based on what details need to be provided

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itemId = self.request.GET.get('item', '')
        # checking if need to display toppings for steak + cheese
        cheeseSteak = True if MenuItem.objects.get(pk=itemId).name.strip() == "Steak + Cheese" else False
        context['category'] = MenuItem.objects.filter(pk=itemId).first().category
        context['cheesesteak'] = cheeseSteak
        return context

class viewCart(ListView):

    template_name = "orders/viewCart.html"

    def get_queryset(self):
        try:
            currentOrder = Order.objects.get(user=self.request.user, completed=False)
        except Order.DoesNotExist:
            currentOrder = None
        return OrderDetail.objects.filter(order = currentOrder)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currentOrder = Order.objects.get(user=self.request.user, completed=False)
        context["paymentPrice"] = currentOrder.total * 100
        return context

class deleteItem(DeleteView):

    model = OrderDetail
    success_url = reverse_lazy("viewCart")
