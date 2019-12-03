from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms import widgets
from webapp.models import Issue, Status, Type, Project, Team
from datetime import datetime


def get_all_project_of_user(user):
    return Project.objects.filter(teams__participant_id=user)


class IssueForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), label='Исполнитель', empty_label='Укажите исполнителя')

    class Meta:
        model = Issue
        exclude = ['created_at', 'created_by', 'project']


class ProjectForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Участники проекта', required=False)

    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at']

    def save(self, commit=True):
        project = super().save()
        self.delete_participants(project)
        self.add_participants(project)
        return project

    def delete_participants(self, project):
        for team in Team.objects.filter(project=project):
            if team.participant not in self.cleaned_data['participants']:
                team.finished_at=datetime.now()
                team.save()

    def add_participants(self, project):
        for participant in self.cleaned_data['participants']:
            team, _ = Team.objects.get_or_create(project=project, participant=participant)
            team.finished_at = None
            team.save()


class ChangeTeamForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label ='Выберите участников проекта', required=False)

    class Meta:
        model = Project
        fields = ['participants']

    def save(self, commit=True):
        project = super().save()
        self.delete_participants(project)
        self.add_participants(project)
        return project

    def delete_participants(self, project):
        for team in Team.objects.filter(project=project):
            if team.participant not in self.cleaned_data['participants']:
                team.finished_at=datetime.now()
                team.save()

    def add_participants(self, project):
        for participant in self.cleaned_data['participants']:
            team, _ = Team.objects.get_or_create(project=project, participant=participant)
            team.finished_at = None
            team.save()


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')