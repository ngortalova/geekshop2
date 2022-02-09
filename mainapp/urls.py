from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.ProductsListView.as_view(), name='index'),
    path('category/<int:pk>/', mainapp.ProductsListView.as_view(), name='category'),
    path('product/<int:pk>/', mainapp.ProductDetailView.as_view(), name='product'),
    # AJAX
    path('product/<int:pk>/ajax/', cache_page(3600)(mainapp.AjaxProductDetailView.as_view()), name='product_ajax'),

]

