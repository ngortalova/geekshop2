from django.db import models
from django.db.models.fields import DecimalField, IntegerField
from django.db.models.fields.related import ForeignKey
import random


class ProductManager(models.Manager):

    @property
    def hot_product(self):
        list_of_products = list(self.filter(is_active=True))
        return random.choice(list_of_products)


class ProductCategory(models.Model):
    name = models.CharField(verbose_name="имя",
                            max_length=64,
                            unique=True)
    description = models.TextField(verbose_name="описание",
                                   blank=True)
    is_active = models.BooleanField(verbose_name="в каталоге", default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = ProductManager()

    name = models.CharField(verbose_name="имя",
                            max_length=128,
                            unique=True)
    description = models.TextField(verbose_name="описание",
                                   blank=True)
    category = ForeignKey(ProductCategory, on_delete=models.SET_NULL,
                          null=True)
    short_description = models.CharField(verbose_name="короткое описание",
                                         max_length=64,
                                         blank=True)
    price = DecimalField(verbose_name="цена",
                         max_digits=8,
                         decimal_places=2,
                         default=0)
    price_with_discount = DecimalField(verbose_name="цена со скидкой",
                                       max_digits=8,
                                       decimal_places=2,
                                       default=0)
    quantity = IntegerField(verbose_name="кол-во на складе",
                            default=0)
    image = models.ImageField(upload_to="products_images",
                              blank=True)
    is_active = models.BooleanField(verbose_name="в каталоге", default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')
