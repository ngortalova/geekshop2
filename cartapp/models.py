from django.db import models
from django.conf import settings
from mainapp.models import Product


class CartManager(models.Manager):
    def has_items(self):
        return bool(len(self.all()))

    @property
    def amount(self):
        return sum(item.quantity for item in self.all())

    @property
    def total_cost(self):
        return sum(item.product.price * item.quantity for item in self.all())


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart",
                             verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=0)
    add_datetime = models.DateTimeField(verbose_name="Время", auto_now_add=True)

    objects = CartManager()

    @classmethod
    def get_items(self, user):
        return Cart.objects.filter(user=user)

    @property
    def cost(self):
        return self.product.price * self.quantity
