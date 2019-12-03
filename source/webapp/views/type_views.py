from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import render
from django.urls import reverse_lazy

from webapp.forms import TypeForm
from webapp.models import Type
from django.views.generic import ListView, CreateView,UpdateView, DeleteView


class TypeListView(ListView):
    model = Type
    template_name = 'type/type_index.html'


class TypeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    extra_context = {'title': 'Типа'}
    model = Type
    form_class = TypeForm
    success_url = reverse_lazy('webapp:types')


class TypeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'update.html'
    extra_context = {'title': 'Типа'}
    model = Type
    form_class = TypeForm
    success_url = reverse_lazy('webapp:types')


class TypeDeleteView(LoginRequiredMixin, DeleteView):
    extra_context = {'title': 'удалить Тип'}
    template_name = 'delete.html'
    model = Type
    success_url = reverse_lazy('webapp:types')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, 'partial/error.html')