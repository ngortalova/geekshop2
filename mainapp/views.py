from django.core.cache import cache
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from datetime import datetime

from django.views.generic import DetailView

from geekshop import settings
from .models import ProductCategory, Product
from django.views.generic.list import ListView

menu_links = [
    {'view_name': 'index', 'active_if': ['index'], 'name': 'домой'},
    {'view_name': 'products:index', 'active_if':
        ['products:index', 'products:category', 'products:product', 'products:page', 'products:hpage'],
     'name': 'продукты'},
    {'view_name': 'contact', 'active_if': ['contact'], 'name': 'контакты'},
]

list_of_products = Product.objects.filter(is_active=True).select_related('category')


class IndexListView(ListView):
    model = Product
    template_name = 'mainapp/index.html'
    paginate_by = 4

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True).order_by("price").select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        context['container_block_class'] = "slider"
        context['menu_links'] = menu_links
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'mainapp/product.html'

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['container_block_class'] = "hero-white"
        data['product_categories'] = get_links_menu()
        data['menu_links'] = menu_links
        return data


class ProductsListView(ListView):
    template_name = 'mainapp/products.html'
    model = Product
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset().select_related('category')
        category_pk = self.kwargs.get('pk')
        if category_pk:
            queryset = queryset.filter(category__pk=category_pk)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        category_pk = self.kwargs.get('pk')
        data['container_block_class'] = "hero-white"
        data['product_categories'] = get_links_menu()
        data['menu_links'] = menu_links
        data['hot_product'] = Product.objects.hot_product
        data['category_pk'] = category_pk

        return data


def contact(request):
    return render(request, 'mainapp/contact.html', context={'menu_links': menu_links,
                                                            'title': 'наши контакты',
                                                            'container_block_class': "hero",
                                                            })


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)
