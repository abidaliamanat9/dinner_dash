from django.db import models
from authentication.models import User
from django.core.validators import MinValueValidator
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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
    photo = CloudinaryField('photo', blank=True, null=True)
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

    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.status}"


class CartItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    quantity = models.IntegerField()
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(pre_delete, sender=Category)
def delete_items_related_to_category(sender, instance, **kwargs):
    items_to_delete = Item.objects.filter(category=instance)
    for item in items_to_delete:
        if item.category.count() == 1:
            item.delete()
