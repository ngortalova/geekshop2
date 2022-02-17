from adminapp.views import category, user, product
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', user.UsersCreateView.as_view(), name='user_create'),
    path('users/read/', user.UsersListView.as_view(), name='users'),
    path('users/update/<int:pk>/', user.UsersUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', user.UsersDeleteView.as_view(), name='user_delete'),

    path('categories/create/', category.CategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', category.CategoriesListView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', category.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', category.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/category/<int:pk>/', product.ProductCreateView.as_view(), name='product_create'),
    path('products/read/category/<int:pk>/', product.ProductsListView.as_view(), name='products'),
    path('products/read/<int:pk>/', product.ProductDetailView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', product.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', product.ProductDeleteView.as_view(), name='product_delete'),
]
