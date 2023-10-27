from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)

class Category(models.Model):
    category = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.category}"
class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ManyToManyField(Category, null=True, related_name="listings")
    available = models.BooleanField()
    stock = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    image_URL = models.URLField(_("Image URL(Optinonal)"),blank=True, max_length=200)
    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.available = False
        elif self.stock != 0:
            self.available = True
        elif not self.image_URL:
            self.image_URL = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930"
        super(Item, self).save(*args, **kwargs)



