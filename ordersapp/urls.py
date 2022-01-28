from django.urls import path

from . import views

app_name = 'ordersapp'

urlpatterns = [
   path('', views.OrderList.as_view(), name='list'),
   path('forming/complete/<pk>', views.order_forming_complete, name='order_forming_complete'),
   path('create/', views.OrderItemsCreate.as_view(), name='create'),
   path('read/<pk>/', views.OrderRead.as_view(), name='read'),
   path('update/<pk>/', views.OrderItemsUpdate.as_view(), name='update'),
   path('delete/<pk>/', views.OrderDelete.as_view(), name='delete'),
   path('product/price/<int:pk>/', views.get_product_price, name='get_product_price'),

]
