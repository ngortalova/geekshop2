from django.urls import path

from . import views

app_name = 'ordersapp'

urlpatterns = [
   path('', views.OrderList.as_view(), name='list'),
   path('create/', views.OrderItemsCreate.as_view(), name='create'),
   path('read/<pk>/', views.OrderItemsCreate.as_view(), name='read'),
   path('update/<pk>/', views.OrderItemsCreate.as_view(), name='update'),
   path('delete/<pk>/', views.OrderItemsCreate.as_view(), name='delete'),

]
