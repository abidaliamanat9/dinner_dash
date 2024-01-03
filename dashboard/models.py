from django.db import models
from authentication.models import User
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Resturant(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    photo = CloudinaryField("photo", blank=True, null=True)
    retired = models.BooleanField(default=False)
    category = models.ManyToManyField(Category)
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return "https://res.cloudinary.com/dtrcsmqle/image/upload/v1704271796/diner-dash_no418d.jpg"


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
    status_changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.status}"


class CartItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    quantity = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.item.title
