from django.test import TestCase
from django.urls import reverse
from . import factories


class OrderDetailViewTestCase(TestCase):
    def setUp(self):
        self.category = factories.CategoryFactory()
        self.item = factories.ItemFactory(categories=[self.category])

    def test_order_detail_view(self):
        self.user = factories.UserFactory()
        self.client.login(email=self.user.email, password="test1234")
        self.order = factories.OrderFactory(user=self.user)
        url = reverse("myorder_detail", kwargs={"order_id": self.order.id})
        self.cartitem = factories.CartItemFactory(
            order=self.order, user=self.user, item=self.item
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_order_notexist_detail_view(self):
        # breakpoint()
        self.acuser = factories.UserFactory(email="abid@devsinc.com")
        self.user = factories.UserFactory(email="ahmad@devsinc.com")
        self.client.login(email=self.user.email, password="test1234")
        self.order = factories.OrderFactory(user=self.acuser)
        url = reverse("myorder_detail", kwargs={"order_id": self.order.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("myorders"))

    def test_order_detail_view_unauthenticated(self):
        self.client.logout()
        self.order = factories.OrderFactory()
        url = reverse("orderdetail", kwargs={"order_id": self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login") + f"?next={url}")
