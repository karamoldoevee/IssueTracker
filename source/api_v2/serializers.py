from webapp.models import Issue

from rest_framework import serializers

class IssueSerializer(serializers.ModelSerializer):

    class Meta:

        model = Issue

        fields = ('id', 'summary', 'description', 'status', 'type', 'created_at', 'project',
                  'created_by', 'assigned_to')
