from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView

from authapp.models import ShopUser
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView


def check_if_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    return True


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(check_if_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'


class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'

        return context


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
