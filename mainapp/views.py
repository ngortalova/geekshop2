from django.shortcuts import render
from django.shortcuts import get_object_or_404
from datetime import datetime

from django.views import View
from django.views.generic import TemplateView

from .models import ProductCategory, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView

menu_links = [
    {'view_name': 'index', 'active_if': ['index'], 'name': 'домой'},
    {'view_name': 'products:index', 'active_if':
        ['products:index', 'products:category', 'products:product', 'products:page', 'products:hpage'],
     'name': 'продукты'},
    {'view_name': 'contact', 'active_if': ['contact'], 'name': 'контакты'},
]

list_of_products = Product.objects.filter(is_active=True)


class IndexListView(ListView):
    model = Product
    template_name = 'mainapp/index.html'
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(is_active=True).order_by("price")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        context['container_block_class'] = "slider"
        context['menu_links'] = menu_links
        return context


def contact(request):
    return render(request, 'mainapp/contact.html', context={'menu_links': menu_links,
                                                            'title': 'наши контакты',
                                                            'container_block_class': "hero",
                                                            })


def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product_categories = ProductCategory.objects.all()
    products_new = Product.objects.filter(category_id=product.category_id, is_active=True)
    return render(request, 'mainapp/product.html', context={'menu_links': menu_links,
                                                            'container_block_class': "hero-white",
                                                            'product': product,
                                                            'product_categories': product_categories,
                                                            'products_new': products_new,
                                                            })


def products(request, pk=None, page=1):
    if not pk:
        selected_category = ProductCategory.objects.first()
    else:
        selected_category = get_object_or_404(ProductCategory, id=pk)

    per_page = request.GET.get('per_page', default='3')
    product_categories = ProductCategory.objects.all()
    products_new = list_of_products.order_by("price").filter(category_id=pk)
    products = list_of_products.order_by("price")
    paginator = Paginator(products, per_page)

    try:
        paginator_page = paginator.page(page)
    except PageNotAnInteger:
        paginator_page = paginator.page(1)
    except EmptyPage:
        paginator_page = paginator.page(paginator.num_pages)

    content = {'menu_links': menu_links,
               'products_new': products_new,
               'container_block_class': "hero-white",
               'product_categories': product_categories,
               'products': paginator_page,
               'page': page,
               'selected_category': selected_category,
               'hot_product': Product.objects.hot_product,
               }

    return render(request, 'mainapp/products.html', content)
