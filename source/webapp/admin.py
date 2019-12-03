from django.contrib import admin
from webapp.models import Issue, Status, Type, Project,Team


class IssueAdmin(admin.ModelAdmin):
    list_display = ['pk', 'summary', 'project', 'status', 'type',  'created_at', 'created_by', 'assigned_to']
    list_filter = ['status', 'type']
    list_display_links = ['pk', 'summary']
    search_fields = ['summary', 'description']
    fields = ['summary', 'description', 'project','status', 'type', 'created_at', 'created_by', 'assigned_to']
    readonly_fields = ['created_at']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'status', 'created_at', 'updated_at']
    list_filter = ['status']
    list_display_links = ['pk', 'name']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Issue, IssueAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Team)
