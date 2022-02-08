from django.urls import path
import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.ProductsListView.as_view(), name='index'),
    path('category/<int:pk>/', mainapp.ProductsListView.as_view(), name='category'),
    path('product/<int:pk>/', mainapp.ProductDetailView.as_view(), name='product'),
    # AJAX
    path('/ajax', mainapp.ProductsListView.as_view(), name='ajax_index'),
    path('category/ajax/<int:pk>/', mainapp.ProductsListView.as_view(), name='ajax_category'),


]

