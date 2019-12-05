from rest_framework import viewsets

from webapp.models import Issue, Project

from api_v2.serializers import IssueSerializer, ProjectSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer