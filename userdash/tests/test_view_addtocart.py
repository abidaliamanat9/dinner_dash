from django.shortcuts import redirect
from django.test import TestCase
from django.urls import reverse
from . import factories
from dashboard.models.cartitem_model import CartItem
from django.contrib.messages import get_messages


class AddToCartViewTestCase(TestCase):
    def setUp(self):
        self.category = factories.CategoryFactory()
        self.resturant = factories.ResturantFactory()
        self.item = factories.ItemFactory(
            categories=[self.category], resturant=self.resturant
        )

    def test_add_to_cart_item_exists_authenticated_user(self):
        self.user = factories.UserFactory()
        self.client.login(email=self.user.email, password="test1234")
        cartitem = factories.CartItemFactory(order=None, user=self.user, item=self.item)
        url = reverse("add_to_cart", kwargs={"item_id": self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("userhome"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "Item already in your cart! quantity is increased by 1"
        )

    def test_add_to_cart_new_item_authenticated_user(self):
        self.user = factories.UserFactory()
        self.item1 = factories.ItemFactory(categories=[self.category])
        self.client.login(email=self.user.email, password="test1234")
        url = reverse("add_to_cart", kwargs={"item_id": self.item1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("userhome"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Item was added to cart successfuly")

    def test_add_to_cart_new_item_resturant_authenticated_user(self):
        self.user = factories.UserFactory()
        self.item1 = factories.ItemFactory(categories=[self.category])
        self.client.login(email=self.user.email, password="test1234")
        cartitem = factories.CartItemFactory(order=None, user=self.user, item=self.item)
        url = reverse("add_to_cart", kwargs={"item_id": self.item1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("userhome"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "You can only add items from one restaurant at a time."
        )

    def test_add_to_cart_item_new_unauthenticated_user(self):
        self.client.logout()
        url = reverse("add_to_cart", kwargs={"item_id": self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("userhome"))
        session_cart = self.client.session.get("cart")
        session_restaurant_id = self.client.session.get("resturant_id")
        self.assertIsNotNone(session_cart)
        self.assertIsNotNone(session_restaurant_id)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Item was added to cart successfuly")

    def test_add_to_cart_item_exists_unauthenticated_user(self):
        # self.client.logout()
        item1 = factories.ItemFactory(categories=[self.category])
        cart = self.client.session.get("cart", [])

        cart.append(
            {
                "id": item1.id,
                "name": item1.title,
                "quantity": 1,
                "price": float(item1.price),
                "stprice": float(item1.price),
            }
        )
        session = self.client.session 
        session["cart"] = cart
        session.save()
        url = reverse("add_to_cart", kwargs={"item_id": item1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("userhome"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Item already in your cart! quantity is increased by 1")


    def test_add_to_cart_new_item_resturant_unauthenticated_user(self):
        item1 = factories.ItemFactory(categories=[self.category])
        cart = self.client.session.get("cart", [])
        resturant = self.client.session.get("resturant_id")
        cart.append(
            {
                "id": self.item.id,
                "name": self.item.title,
                "quantity": 1,
                "price": float(self.item.price),
                "stprice": float(self.item.price),
            }
        )
        session = self.client.session 
        session["cart"] = cart
        session["resturant_id"] = self.item.resturant.id
        session.save()
        url = reverse("add_to_cart", kwargs={"item_id": item1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("userhome"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "You can only add items from one restaurant at a time."
        )


    def test_item_not_exist(self):
        url = reverse("add_to_cart", kwargs={"item_id": 20})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("userhome"))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "This Item is not existing")
