from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from cartapp.models import Cart
from mainapp.models import Product
from ordersapp.forms import OrderItemForm, OrderForm
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
                    form.initial['price'] = cart_items[num].product.price
                    form.initial['sum_price'] = form.initial['price']  * form.initial['quantity']
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            Cart.objects.filter(user=self.request.user).delete()
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order,
                                             OrderItem,
                                             form=OrderItemForm,
                                             extra=1)
        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                    form.initial['sum_price'] = form.instance.product.price * form.initial['quantity']
            data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderRead, self).get_context_data(**kwargs)
        context['title'] = 'заказ/просмотр'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:list'))


def get_product_price(request, pk):
    if request.is_ajax:
        product_item = Product.objects.filter(pk=pk).first()
        if product_item:
            return JsonResponse({"price": product_item.price})
        return JsonResponse({"price": 0})

