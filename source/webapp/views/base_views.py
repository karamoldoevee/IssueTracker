from django.db.models import ProtectedError
from django.utils.http import urlencode
from django.views.generic import TemplateView, View, ListView
from django.shortcuts import get_object_or_404, render, redirect


class DetailView(TemplateView):
    context_key = 'object'
    model = None

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context[self.context_key] = get_object_or_404(self.model, pk=pk)
        return context


class UpdateView(View):
    form_class = None
    template_name = None
    model = None
    redirect_url = None
    key_kwarg = 'pk'
    extra_context = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object)
        return render(request, self.template_name, context={'form': form, **self.extra_context})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_redirect_url(self):
        return self.redirect_url

    def form_valid(self, form):
        form.save()
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        return render(self.request, self.template_name, context={'form': form})

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)


class DeleteView(View):
    template_name = None
    confirm_delete = True
    model = None
    redirect_url = None
    key_kwarg = 'pk'
    extra_context = None
    failure_template_name = None

    def get_object(self):
        pk = self.kwargs.get(self.key_kwarg)
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.confirm_delete:
            return render(request, self.template_name, context={'object': self.object, **self.extra_context})
        else:
            return self.delete_object(request)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.delete_object(request)

    def delete_object(self, request):
        try:
            self.object.delete()
            return redirect(self.redirect_url)
        except ProtectedError:
            return render(request, self.failure_template_name)


class SearchView(ListView):
    search_form = None

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['search'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_search_form(self):
        return self.search_form(data=self.request.GET)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(
                self.get_filters()
            )
        return queryset

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_filters(self):
        pass

