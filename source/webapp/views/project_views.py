from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.urls import reverse, reverse_lazy
from webapp.models import Project, PROJECT_DEFAULT_STATUS, Team
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from webapp.forms import ProjectForm, SimpleSearchForm, IssueForm, ChangeTeamForm
from webapp.views.base_views import SearchView
from webapp.views.issue_views import get_all_project_of_user, get_participants_of_project


class ProjectListView(SearchView):
    model = Project
    template_name = 'project/project_index.html'
    search_form = SimpleSearchForm
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_projects'] = self.get_queryset().filter(status='active')
        context['closed_projects'] = self.get_queryset().filter(status='closed')
        if self.request.user.is_authenticated:
            context['editable_projects'] = get_all_project_of_user(self.request.user)
        return context

    def get_filters(self):
        return Q(name__icontains=self.search_value)


class ProjectDetailView(DetailView):
    template_name = 'project/project.html'
    context_key = 'project'
    model = Project

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status != PROJECT_DEFAULT_STATUS:
            raise Http404('Указанный проект не найден...')
        else:
            return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        issues = project.issues.order_by('-created_at')
        context['can_edit'] = self.request.user.is_authenticated and \
                              project in get_all_project_of_user(self.request.user)
        form = IssueForm()
        form.fields['assigned_to'].queryset = get_participants_of_project(project).exclude(id=self.request.user.id)
        context['form'] = form
        context['teams'] = Team.objects.filter(project=project).filter(finished_at=None)
        self.paginate_comments_to_context(issues, context)
        return context

    def paginate_comments_to_context(self, issues, context):
        paginator = Paginator(issues, 2, 0)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page
        context['issues'] = page.object_list
        context['is_paginated'] = page.has_other_pages()


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'create.html'
    extra_context = {'title': 'Проекта'}
    success_url = reverse_lazy('webapp:projects')
    permission_required = 'webapp.add_project'
    permission_denied_message = '403 Доступ запрещен!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['participants'].queryset = form.fields['participants'].queryset.exclude(id = self.request.user.id)
        return form

    def form_valid(self, form):
        user = User.objects.filter(id=self.request.user.id)
        form.cleaned_data['participants'] = form.cleaned_data['participants'].union(user)
        return super().form_valid(form)


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = 'update.html'
    extra_context = {'title': 'Проекта'}
    permission_required = 'webapp.change_project'
    permission_denied_message = '403 Доступ запрещен!'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status != PROJECT_DEFAULT_STATUS:
            raise Http404('Указанный проект не найден...')
        else:
            return super().get(self,request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['participants'].queryset = form.fields['participants'].queryset.exclude(id=self.request.user.id)
        return form

    def form_valid(self, form):
        user = User.objects.filter(id=self.request.user.id)
        form.cleaned_data['participants'] = form.cleaned_data['participants'].union(user)
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.status == PROJECT_DEFAULT_STATUS:
            return reverse('webapp:project_view', kwargs={'pk': self.object.pk})
        else:
            return reverse('webapp:projects')


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:projects')
    extra_context = {'title': 'закрыть Проект'}
    permission_required = 'webapp.delete_project'
    permission_denied_message = '403 Доступ запрещен!'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status != PROJECT_DEFAULT_STATUS:
            raise Http404('Указанный проект не найден...')
        else:
            return super().get(self,request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.status = 'closed'
        self.object.save()
        return HttpResponseRedirect(success_url)


class ChangeTeamView(PermissionRequiredMixin, UpdateView):
    form_class = ChangeTeamForm
    model = Project
    template_name = 'update.html'
    extra_context = {'title': 'Команды'}
    permission_required = 'webapp.change_team'
    permission_denied_message = '403 Доступ запрещен!'
    success_url = reverse_lazy('webapp:projects')

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['participants'].queryset = form.fields['participants'].queryset.exclude(id=self.request.user.id)
        return form

    def form_valid(self, form):
        user = User.objects.filter(id=self.request.user.id)
        form.cleaned_data['participants'] = form.cleaned_data['participants'].union(user)
        return super().form_valid(form)
