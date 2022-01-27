from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView

from mainapp.models import Product
from .models import Cart
from django.contrib.auth.decorators import login_required


class CartTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cartapp/cart.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart_items'] = self.request.user.cart.all()

        return context


@login_required
def add_to_cart(request, pk=None):
    product = get_object_or_404(Product, pk=pk)

    cart_product = request.user.cart.filter(id=pk).first()

    if not cart_product:
        cart_product = Cart(user=request.user, product=product)

    cart_product.quantity += 1
    cart_product.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    cart_item.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def api_edit_cart(request, pk, quantity):
    quantity = int(quantity)
    new_cart_item = Cart.objects.get(pk=int(pk))

    if quantity > 0:
        new_cart_item.quantity = quantity
        new_cart_item.save()
    else:
        new_cart_item.delete()

    cart_items = Cart.objects.filter(user=request.user).order_by('product__category')

    content = {
        'cart_items': cart_items,
    }

    result = render_to_string('cartapp/includes/inc_cart_list.html', content)

    return JsonResponse({'result': result})


# @receiver(pre_save, sender=Cart)
# def product_quantity_update_save(sender, update_fields, instance, **kwargs):
#     if update_fields is 'quantity' or 'product':
#         if instance.pk:
#             instance.product.quantity -= instance.quantity - \
#                                          sender.get_item(instance.pk).quantity
#         else:
#             instance.product.quantity -= instance.quantity
#         instance.product.save()


@receiver(pre_delete, sender=Cart)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


