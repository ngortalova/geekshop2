from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from cartapp.models import Cart
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem

from django.forms import inlineformset_factory


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            cart_items = Cart.get_items(self.request.user)
            if len(cart_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(cart_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = cart_items[num].product
                    form.initial['quantity'] = cart_items[num].quantity
                cart_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)
