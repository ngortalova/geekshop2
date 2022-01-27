from django.urls import path

import cartapp.views
from . import views

app_name = 'cartapp'

urlpatterns = [
   path('', views.CartTemplateView.as_view(), name='view'),
   path('add/<int:pk>', views.add_to_cart, name='add_to_cart'),
   path('remove/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
   path('api/edit/<int:pk>/<int:quantity>/', views.api_edit_cart, name='edit')

]
