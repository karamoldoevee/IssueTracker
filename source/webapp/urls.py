from django.urls import path
from webapp.views import IndexView, IssueCreateView, IssueView, IssueUpdateView, IssueDeleteView, \
    StatusListView, StatusCreateView, StatusDeleteView, StatusUpdateView, TypeListView, TypeCreateView, \
    TypeDeleteView, TypeUpdateView, ProjectListView, ProjectCreateView, ProjectDetailView, \
    ProjectUpdateView, ProjectDeleteView, ChangeTeamView
urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('issue/<int:pk>/', IssueView.as_view(), name='issue_view'),
    path('issue/create/<int:project_pk>', IssueCreateView.as_view(), name='issue_create'),
    path('issue/update/<int:pk>/', IssueUpdateView.as_view(), name='issue_update'),
    path('issue/delete/<int:pk>/', IssueDeleteView.as_view(), name='issue_delete'),
    path('statuses/', StatusListView.as_view(), name='statuses'),
    path('status/create/', StatusCreateView.as_view(), name='status_create'),
    path('status/update/<int:pk>/', StatusUpdateView.as_view(), name='status_update'),
    path('status/delete/<int:pk>/', StatusDeleteView.as_view(), name='status_delete'),
    path('types/', TypeListView.as_view(), name='types'),
    path('types/create/', TypeCreateView.as_view(), name='type_create'),
    path('type/update/<int:pk>/', TypeUpdateView.as_view(), name='type_update'),
    path('type/delete/<int:pk>/', TypeDeleteView.as_view(), name='type_delete'),
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_view'),
    path('project/update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('team/update/<int:pk>', ChangeTeamView.as_view(), name='team_update')

]

app_name = 'webapp'
