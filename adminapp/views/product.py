from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from mainapp.models import Product
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator


def check_if_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 2

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])

    @method_decorator(user_passes_test(check_if_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['id'] = self.object.category.id

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product.html'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context['id'] = self.object.category.id
        return context

    @method_decorator(user_passes_test(check_if_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
