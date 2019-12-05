from rest_framework import viewsets

from webapp.models import Issue

from api_v2.serializers import IssueSerializer

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer