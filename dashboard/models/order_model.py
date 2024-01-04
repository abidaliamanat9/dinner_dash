from django.db import models
from authentication.models import User
from dashboard.models.item_model import Item


class Order(models.Model):
    STATUS_CHOICES = [
        ("ORDERED", "Ordered"),
        ("PAID", "Paid"),
        ("CANCELLED", "Cancelled"),
        ("COMPLETED", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through="CartItem")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ORDERED")
    status_changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.status}"
