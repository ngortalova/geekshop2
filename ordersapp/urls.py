from django.urls import path

from . import views

app_name = 'ordersapp'

urlpatterns = [
   path('', views.orders_list, name='view'),
]
