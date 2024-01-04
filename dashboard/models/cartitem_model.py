from django.db import models
from authentication.models import User
from dashboard.models.item_model import Item
from dashboard.models.order_model import Order


class CartItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    quantity = models.IntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.item.title
