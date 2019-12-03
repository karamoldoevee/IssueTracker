from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import render
from django.urls import reverse_lazy

from webapp.forms import StatusForm
from webapp.models import Status
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


class StatusListView(ListView):
    model = Status
    template_name = 'status/status_index.html'


class StatusCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create.html'
    extra_context = {'title': 'Статуса'}
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('webapp:statuses')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'update.html'
    extra_context = {'title': 'удалить Статус'}
    model = Status
    fields = ['name']
    success_url = reverse_lazy('webapp:statuses')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    extra_context = {'title': 'Статус'}
    model = Status
    success_url = reverse_lazy('webapp:statuses')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            return render(request, 'partial/error.html')