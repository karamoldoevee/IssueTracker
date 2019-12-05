from webapp.models import Issue, Project

from rest_framework import serializers


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ('id', 'summary', 'description', 'status', 'type', 'created_at', 'project', 'created_by', 'assigned_to')

class ProjectIssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ('id', 'summary', 'description', 'status', 'type', 'created_at', 'created_by', 'assigned_to')

class ProjectSerializer(serializers.ModelSerializer):
    issues = ProjectIssueSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at', 'updated_at', 'status', 'issues')