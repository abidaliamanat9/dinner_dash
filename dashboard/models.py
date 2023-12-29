from django.db import models
from authentication.models import User
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(limit_value=1, message="Price must be greater than zero.")
        ],
    )
    photo = CloudinaryField("photo", blank=True, null=True)
    retired = models.BooleanField(default=False)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        ("ORDERED", "Ordered"),
        ("PAID", "Paid"),
        ("CANCELLED", "Cancelled"),
        ("COMPLETED", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField("Item", through="CartItem")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ORDERED")
    status_changed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.status}"


class CartItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    quantity = models.IntegerField()
    stprice = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
