from django.test import TestCase
from django.urls import reverse
from dashboard.models.cartitem_model import CartItem, Order
from . import factories
from django.contrib.messages import get_messages


class CheckOutViewTest(TestCase):
    def setUp(self):
        self.category = factories.CategoryFactory()
        self.item = factories.ItemFactory(categories=[self.category])

    def test_checkout_with_items(self):
        self.user = factories.UserFactory()
        self.client.login(email=self.user.email, password="test1234")
        url = reverse("checkout")
        cartitem = factories.CartItemFactory(order=None, user=self.user, item=self.item)
        order = factories.OrderFactory(user=self.user)
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("myorders"))
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your Order is placed successfuly")

    def test_checkout_with_empty_cart(self):
        url = reverse("checkout")
        self.nuser = factories.UserFactory()
        self.client.login(email=self.nuser.email, password="test1234")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        print(self.nuser.id)
        # messages = list(get_messages(response.wsgi_request))
        # self.assertEqual(len(messages), 1)
        # self.assertEqual(
        #     str(messages[0]), "You cart is empty! Order is not placed with empty cart"
        # )

    def test_checkout_redirects_to_login(self):
        self.client.logout()
        url = reverse("checkout")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login") + f"?next={url}")
