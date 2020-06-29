from django.test import Client, TestCase, RequestFactory

from .models import Order, MenuItem, OrderDetail, Category, PizzaTopping, CheesesteakTopping
from .views import addItemForm, viewCart
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your tests here.
class OrderTestCases(TestCase):
    #*****************************# print(response.context["form"].errors) <-- useful for debugging CBV POST errors
    def setUp(self):

        # create test categories
        testCategoryPizza = Category.objects.create(name="PZA")
        testCategoryPasta = Category.objects.create(name="PST")
        testCategorySandwich = Category.objects.create(name="SUB")

        # create test menu items
        testPizza = MenuItem.objects.create(name="2 Topping Pizza", priceSmall=5, priceLarge=10, pizzaStyle="NML", pizzaToppingsCount=2, category=testCategoryPizza)
        testPasta = MenuItem.objects.create(name="Pasta Bolognese", priceSmall=8, priceLarge=8, category=testCategoryPasta)
        testCheeseSteak = MenuItem.objects.create(name="Cheesesteak", priceSmall=7.50, priceLarge=11.25, category=testCategorySandwich)
        testBurger = MenuItem.objects.create(name="Hamburger", priceSmall=6, priceLarge=9, category=testCategorySandwich)

        # create test Toppings
        testPizzaTopping1 = PizzaTopping.objects.create(name="Mushroom")
        testPizzaTopping2 = PizzaTopping.objects.create(name="Pepperoni")
        testSubTopping1 = CheesesteakTopping.objects.create(name="MSH")
        testSubTopping2 = CheesesteakTopping.objects.create(name="GPP")

        # create test user
        testUser = User(username="test", email="test@test.com")
        testUser.set_password("test")
        testUser.is_staff = True
        testUser.save()

        #create test order
        testOrder = Order.objects.create(user=testUser)

        #create test order details
        testDetail1 = OrderDetail.objects.create(order=testOrder, item=testPizza, size="LG", quantity=1)
        testDetail1.toppings.add(testPizzaTopping1, testPizzaTopping2)

        testDetail2 = OrderDetail.objects.create(order=testOrder, item=testPasta, quantity=2, notes="Extra cheese please")

        testDetail3 = OrderDetail.objects.create(order=testOrder, item=testCheeseSteak, size="LG", quantity=1, extraCheese=True)
        testDetail3.sandwichToppings.add(testSubTopping1, testSubTopping2)

        # for simulating browser requests
        self.client = Client()


    # test models
    def testPizzaToppingsAdd(self):
        pizza = MenuItem.objects.get(name="2 Topping Pizza")
        pizzaOrderDetail = OrderDetail.objects.get(item=pizza)
        self.assertEqual(pizzaOrderDetail.toppings.count(), 2)

    def testSandwichToppingsAdd(self):
        cheesesteak = MenuItem.objects.get(name="Cheesesteak")
        subOrderDetail = OrderDetail.objects.get(item=cheesesteak)
        self.assertEqual(subOrderDetail.sandwichToppings.count(), 2)

    def testItemTotaling(self):
        user = User.objects.get(username="test")
        order = Order.objects.get(user=user)
        orderDetails = OrderDetail.objects.filter(order=order)
        orderDetailSum = 0

        for detail in orderDetails:
            itemTotal = detail.updateTotal()
            orderDetailSum += itemTotal

        order.updateTotal()

        self.assertEqual(order.total, orderDetailSum)

    def testOrderCompletion(self):
        user = User.objects.get(username="test")
        order = Order.objects.get(user=user)
        self.assertFalse(order.checkedOut, order.completed)

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_menu_display(self):
        response = self.client.get("/loadMenu")
        self.assertEqual(response.status_code, 200)

    def test_login_redirect(self):
        # if a user tries to add a menu item to their cart they should be directed to login page
        response = self.client.get("/addGeneralItem/1/")
        self.assertEqual(response.status_code, 302)

    def test_user_login(self):
        loginResult = self.client.login(username="test", password="test")
        self.assertEqual(loginResult, True)

    def test_view_cart(self):
        user = User.objects.get(username="test")
        self.client.force_login(user)
        response = self.client.get(reverse('viewCart'), HTTP_REFERER='http://foo/bar')
        print(response.context_data['orderdetail_list'].count())
        self.assertEqual(response.status_code, 200)

    def test_view_cart_item_count(self):
        user = User.objects.get(username="test")
        self.client.force_login(user)
        response = self.client.get(reverse('viewCart'), HTTP_REFERER='http://foo/bar')
        self.assertEqual(response.context_data['orderdetail_list'].count(), 3)

    def test_item_add(self):
        user = User.objects.get(username="test")
        self.client.force_login(user)
        order = Order.objects.get(user=user)
        burger = MenuItem.objects.get(name="Hamburger")
        response = self.client.post(reverse("addGeneralItem", kwargs={'pk': burger.id}), {"order": order.id, "item": burger.id, "quantity": 2, 'size': "LG"})
        self.assertEqual(order.items.all().count(), 4)

    def test_item_delete(self):
        user = User.objects.get(username="test")
        self.client.force_login(user)
        itemToDelete = OrderDetail.objects.first()
        response = self.client.post(reverse("deleteOrderItem", kwargs={'pk': itemToDelete.id}))
        self.assertEqual(Order.objects.first().items.count(), 2)

    def test_item_update(self):
        user = User.objects.get(username="test")
        self.client.force_login(user)
        itemToUpdate = OrderDetail.objects.first()
        response = self.client.post(reverse("editItem", kwargs={'pk': itemToUpdate.id}), {"order": itemToUpdate.order.id, "item": itemToUpdate.item.id, "quantity": 5})
        itemToUpdate.refresh_from_db()
        self.assertEqual(itemToUpdate.quantity, 5)

    def test_Order_Delete(self):
        user = User.objects.get(username="test")
        self.client.force_login(user)
        orderToDelete = Order.objects.first()
        response = self.client.post(reverse("deleteOrder", kwargs={'pk': orderToDelete.id}))
        self.assertEqual(Order.objects.all().count(), 0)

    def test_order_completion(self):
        user = User.objects.get(username="test")
        self.client.force_login(user)
        orderToComplete = Order.objects.first()
        response = self.client.get(reverse("markOrderComplete", kwargs={'pk': orderToComplete.id}))
        self.assertEqual(response.status_code, 302)
        orderToComplete.refresh_from_db()
        self.assertEqual(orderToComplete.completed, True)
