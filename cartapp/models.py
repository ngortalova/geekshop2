from django.utils.functional import cached_property

from django.db import models
from django.conf import settings
from mainapp.models import Product


class CartManager(models.Manager):
    def has_items(self):
        return bool(len(self.all()))

    @property
    def amount(self):
        return sum(item.quantity for item in self.all().select_related())

    @property
    def _total_cost(self):
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
        return Cart.objects.filter(user=user).select_related()

    def cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return Cart.objects.get(pk=pk)

    @cached_property
    def get_items_cached(self):
        return self.user.cart.select_related()

    @property
    def total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    @property
    def total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.cost(), _items)))
