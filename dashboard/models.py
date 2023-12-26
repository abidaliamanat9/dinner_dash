from django.db import models
from django.core.validators import MinValueValidator
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=255,unique = True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2,validators=[MinValueValidator(limit_value=1, message="Price must be greater than zero.")],)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    category = models.ManyToManyField(Category)
    
    
    def __str__(self):
        return self.title


