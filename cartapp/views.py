from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
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
