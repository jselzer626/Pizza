from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.forms import ModelForm, Textarea
from django.contrib.auth.decorators import login_required
from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import StrictButton
import stripe
import json

# Create your views here.
def index(request):
    return render(request, "orders/index.html")

def loadMenu(request):

    context = {
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

class editItem(UpdateView):
    model = OrderDetail
    form_class = addItemForm
    template_name = "orders/editItem.html"
    success_url = reverse_lazy("viewCart")

    def form_valid(self, form):
        form.instance.updateTotal()
        return super().form_valid(form)

class addGeneralItem(CreateView):
    model = OrderDetail
    form_class = addItemForm
    success_url = reverse_lazy("viewCart")

    def get_initial(self):

        try:
            currentOrder = Order.objects.get(user=self.request.user, completed=False)
        except Order.DoesNotExist:
            currentOrder = Order(user=self.request.user)
            currentOrder.save()
        return {'order': currentOrder,
                'item': self.kwargs['pk']}

    # update item total based on selections made in form
    def form_valid(self, form):
        form.instance.updateTotal()
        return super().form_valid(form)

    # this provides the item category so the view can be filtered based on what details need to be provided

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = MenuItem.objects.get(pk=self.kwargs['pk'])
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
        origin = self.request.headers['Referer']
        context = super().get_context_data(**kwargs)
        currentOrder = Order.objects.get(user=self.request.user, completed=False)
        context['message'] = "Item added!" if "add" in origin else ("Item updated!" if "edit" in origin else ("Item deleted!" if 'view' in origin else ''))
        context["paymentPrice"] = currentOrder.total * 100
        return context

class orderList(ListView):

    model = Order
    template_name = "orders/viewOrders.html"

class deleteItem(DeleteView):

    model = OrderDetail
    success_url = reverse_lazy("viewCart")
