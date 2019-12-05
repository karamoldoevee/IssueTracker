from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.urls import reverse, reverse_lazy
from webapp.models import Issue, Project
from webapp.forms import IssueForm, SimpleSearchForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from webapp.views.base_views import SearchView


def get_all_project_of_user(user):
    return Project.objects.filter(teams__participant_id=user)


def get_participants_of_project(project):
    return User.objects.filter(teams__project=project, teams__finished_at=None)


class IndexView(SearchView):
    template_name = 'issue/index.html'
    model = Issue
    context_object_name = 'issues'
    paginate_by = 4
    paginate_orphans = 0
    page_kwarg = 'page'
    ordering = ['-created_at']
    search_form = SimpleSearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            context['editable_projects'] = get_all_project_of_user(self.request.user)
        return context

    def get_filters(self):
        return Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)


class IssueView(DetailView):
    template_name = 'issue/issue.html'
    context_key = 'issue'
    model = Issue

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['can_edit'] = self.request.user.is_authenticated and \
                              self.object.project in get_all_project_of_user(self.request.user)
        return context


class IssueCreateView(UserPassesTestMixin, PermissionRequiredMixin, CreateView):
    form_class = IssueForm
    model = Issue
    template_name = 'create.html'
    extra_context = {'title': 'Задачи'}
    permission_denied_message = 'Доступ запрещен!'
    permission_required = 'webapp.add_issue'

    def get_success_url(self):
        return reverse('webapp:issue_view', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None):
        form = super().get_form()
        project = self.get_project()
        form.fields['assigned_to'].queryset = get_participants_of_project(project=project).exclude(
            id=self.request.user.id)
        return form

    def form_valid(self, form):
        project = self.get_project()
        if not (project in get_all_project_of_user(self.request.user)):
            raise Http404('Вы не можете добавлять задачу в этот проект')
        else:
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.project = project
            return super().form_valid(form)

    def test_func(self):
        project = self.get_project()
        return project in (get_all_project_of_user(self.request.user))

    def get_project(self):
        return Project.objects.get(pk=self.kwargs.get('project_pk'))


class IssueUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    form_class = IssueForm
    model = Issue
    template_name = 'update.html'
    extra_context = {'title': 'Задачи'}
    permission_denied_message = 'Доступ запрещен!'
    permission_required = 'webapp.change_issue'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['assigned_to'].queryset = get_participants_of_project(project=self.object.project).exclude(
            id=self.request.user.id)
        return form

    def get_success_url(self):
        return reverse('webapp:issue_view', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.get_object().project in (get_all_project_of_user(self.request.user))


class IssueDeleteView(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    model = Issue
    template_name = 'delete.html'
    success_url = reverse_lazy('webapp:index')
    extra_context = {'title': 'удалить Задачу'}
    permission_denied_message = 'Доступ запрещен!'
    permission_required = 'webapp.delete_issue'

    def test_func(self):
        return self.get_object().project in get_all_project_of_user(self.request.user)