from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from webapp.models import Issue, Project

from api_v2.serializers import IssueSerializer, ProjectSerializer

from rest_framework.permissions import AllowAny, DjangoModelPermissions, IsAuthenticated

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAuthenticated(), DjangoModelPermissions()]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        else:
            return [IsAuthenticated(), DjangoModelPermissions()]


class LogoutView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            user.auth_token.delete()

        return Response({'status': 'ok'})