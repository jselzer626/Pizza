from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.forms import ModelForm, Textarea
from django.contrib.auth.decorators import login_required
from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import StrictButton
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def index(request):
    return render(request, "orders/index.html")

def loadMenu(request):

    context = {
        'categories': Category.objects.all()
    }
    return render(request, "orders/create.html", context)

def manageOrders(request, msg=''):

    context = {
        'orders': Order.objects.all(),
        'msg': msg,
        'pending': Order.objects.filter(checkedOut=True, completed=False).count()
    }

    return render(request, "orders/manageOrders.html", context)

def markOrderComplete(request, pk):

    orderToComplete = Order.objects.get(pk=pk)
    orderToComplete.completed = True
    orderToComplete.save()
    confirm_address = orderToComplete.user.email
    site = 'http://localhost:8000'
    html_message = render_to_string('orders/orderReceipt.html', {'order': orderToComplete, 'site': site})
    plain_message = strip_tags(html_message)
    send_mail("Thanks!", plain_message, "jselzer1@montgomerycollege.edu", [confirm_address], fail_silently=False, html_message=html_message)

    return HttpResponseRedirect(reverse("manageOrders", kwargs={"msg": "Order Completed!"}))

def showAboutPage(request):

    return render(request, "orders/about.html")

def checkOut(request, pk, orderMethod):

    currentOrder = Order.objects.get(pk=pk)
    currentOrder.checkedOut = True
    currentOrder.method = orderMethod
    currentOrder.save()
    context = {
        'order': currentOrder
    }
    return render(request, "orders/orderConfirmation.html", context)

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

class addGeneralItem(LoginRequiredMixin, CreateView):
    login_url = "/users/"
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
        try:
            currentOrder = Order.objects.get(user=self.request.user, completed=False)
        except Order.DoesNotExist:
            currentOrder = None
        context['message'] = "Item added!" if "add" in origin else ("Item updated!" if "edit" in origin else ("Item deleted!" if 'view' in origin else ''))
        return context

class deleteItem(DeleteView):

    model = OrderDetail
    success_url = reverse_lazy("viewCart")

class deleteOrder(DeleteView):

    model = Order
    success_url = reverse_lazy("manageOrders", kwargs={"msg": "Order Deleted!"})
