from django.urls import path, re_path, include

import mainapp.views as mainapp
from geekshop import settings

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.ProductsListView.as_view(), name='index'),
    path('category/<int:pk>/', mainapp.ProductsListView.as_view(), name='category'),
    path('product/<int:pk>/', mainapp.ProductDetailView.as_view(), name='product'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
