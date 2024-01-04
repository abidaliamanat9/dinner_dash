from django.db import models
from cloudinary.models import CloudinaryField
from dashboard.models.category_model import Category
from dashboard.models.resturant_model import Resturant


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
